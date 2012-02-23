/*
 * ParseProductDSL.scala
 *        written for the sortable coding challenge 
 *        submitted by: Raymund Rimando
 *  usage: scala ParseProductDSL <product.txt> <listing.txt> <output.txt>
 */
import scala.util.parsing.combinator._
import scala.collection.mutable.ListBuffer
import scala.collection.mutable.Buffer
import java.io.FileReader
import java.io.FileWriter

import scala.util.matching.Regex

/* todo: build infrastructure
         packaging
         split into separate files
         unit testing
         */

class ParseErrorException extends java.lang.RuntimeException {
  def this(msg:String) = { this()
    println("msg: " + msg)
  }
}


/* class to instantiate each product */
class Product (val name:String, val manufacturer:String, val model:String, val family:String, val date:String) {
  val resellers:Buffer[Listing] = new ListBuffer[Listing]
  def this(name:String) = this(name, null, null, null, null)

  override def toString = "{\"product_name\":" + name + 
             ",\n \"model\":" + model +
             ",\n \"listings\": [" +  resellers.toArray.deep.mkString(",")  + "\n]},\n"  
}

/* class to instantiate for each listing */
class Listing (val title:String, val manufacturer:String, val currency:String, val price:String) {
  override def toString =  "\n   {\"title\":" + title + ", \"manufacturer\":" + manufacturer + ", \"currency\":" + currency + ", \"price\":" + price +"}"
}

/* compilation of products */
class ProductCatalog {
  private val products:Buffer[Product] = new ListBuffer[Product]

  def this (l: List[Product]) {
    this()
    addListOfProducts(l)
  }

  def addListOfProducts(newProducts:List[Product]) = {
    products ++= newProducts
    this
  }
  def findProductsByManufacturer(n:String): Seq[Product] = {
    products.filter(_.manufacturer.contains(n))
  }

  def getProductList(): Seq[Product] = products 

  def addProductListing(newListing: Listing): Any = {

    /* model delimiter */
    val modelDelimiter = """[ _\-\s/]"""

    /* iterate through the product list by manufacturer */ 
    for (i <- this.findProductsByManufacturer(newListing.manufacturer)) {

      /* trim the double quotes...must be a faster way to do this */
      val modelToken = i.model.tail.dropRight(1)

      /* regex to match the model in the title */
      val modelR = new Regex (".*" + modelDelimiter + "(" + modelToken + ")" + modelDelimiter + ".*")

      newListing.title match {
        case modelR (tmp) => { i.resellers += newListing }
        case _ => // Do nothing
      }                                                                                                              
    }
    this
  }

  override def toString = products.mkString
}

/* compilation of suppler */
class SupplierCatalog {
  private val listing:Buffer[Listing] = new ListBuffer[Listing]
  def this (l: List[Listing]) {
    this()
    addListing(l)
  }

  def getProductList(): Seq[Listing] = listing 

  def addListing(newListing:List[Listing]) = {
    listing ++= newListing
    this
  }
  def findProductsByManufacturer(n:String): Seq[Listing] = {
    listing.filter(_.manufacturer.contains(n))
  }

  def findProductsByTitle(n:String): Seq[Listing] = {
    listing.filter(_.title.contains(n))
  }

  override def toString = "Products: " + listing.mkString
}

object ProductDSL  extends JSONDictionary {
    def ParseProductFile(file:String): ProductCatalog = {
      val reader = new FileReader(file)
      parseAll(catalog, reader) match {
        case Success(result, _) => { new ProductCatalog(result) }
        case Failure(msg, _) => throw new ParseErrorException(msg)
        case Error(msg, next) => throw new ParseErrorException(msg + " : " + next)
      }
    }

    def catalog: Parser[List[Product]] = rep(device) ^^ { productList: List[Product] => productList }

    def device: Parser[Product] = "{" ~ product ~ manufacturer ~ model ~ opt(family) ~ announcedDate ~ "}" ^^ { 
        case "{" ~ product ~ manufacturer ~ model ~ Some(family) ~ announcedDate ~ "}" => { new Product(product, manufacturer, model, family, announcedDate)}
        case "{" ~ product ~ manufacturer ~ model ~ _ ~ announcedDate ~ "}" => {new Product(product, manufacturer, model, null, announcedDate)}
      }
}

object ListingDSL extends JSONDictionary {
    def ParseProductFile(file:String): SupplierCatalog = {
      val reader = new FileReader(file)
      parseAll(catalog, reader) match {
        case Success(result, _) => new SupplierCatalog(result)
        case Failure(msg, _) => throw new ParseErrorException(msg)
        case Error(msg, _) => throw new ParseErrorException(msg)
      }
    }

    def catalog: Parser[List[Listing]] = rep(device) ^^
     { productList: List[Listing] => productList }

    def device: Parser[Listing] = "{" ~ title ~ manufacturer ~ currency ~ price ~ "}" ^^ 
      { case "{" ~ title ~ manufacturer ~ currency ~ price ~ "}" => {new Listing(title, manufacturer, currency, price)} }
}

// parsing literals for JSON dictionary
class JSONDictionary extends JavaTokenParsers {
    // derived from stringLiteral
    def titleLiteral: Parser[String] =  ("\""+"""([\\"]{2}|[^"\p{Cntrl}\\]|\\[\\/bfnrt]|\\u[a-fA-F0-9]{4})*"""+"\"").r

    def title: Parser[String] = { "\"title\"" ~ ":" ~ titleLiteral  ~ "," ^^ {case "\"title\"" ~ ":" ~ title ~ "," => title } }

    def currency: Parser[String] = "\"currency\"" ~ ":" ~ titleLiteral ~ "," ^^ {case "\"currency\"" ~ ":" ~ currency ~ "," => currency } 
    // TODO : convert to float
    def price: Parser[String] = "\"price\"" ~ ":" ~ titleLiteral  ^^ {case "\"price\"" ~ ":" ~ price => price }

    def product: Parser[String] = "\"product_name\"" ~ ":" ~ titleLiteral ~ "," ^^ {case "\"product_name\"" ~ ":" ~ pname ~ "," => pname }

    def manufacturer: Parser[String] = "\"manufacturer\"" ~ ":" ~ titleLiteral ~ "," ^^ {case "\"manufacturer\"" ~ ":" ~ manufacturer ~ "," => manufacturer }

    def model: Parser[String] = "\"model\"" ~ ":" ~ titleLiteral ~ "," ^^ {case "\"model\"" ~ ":" ~ model ~ "," => model }

    def family: Parser[String] = "\"family\"" ~ ":" ~ titleLiteral ~ "," ^^ {case "\"family\"" ~ ":" ~ family ~ "," => family }

    def announcedDate: Parser[String] = "\"announced-date\"" ~ ":" ~ titleLiteral ^^ {case "\"announced-date\"" ~ ":" ~ announcedDate => announcedDate }
}


/* heres the entry point */
object ParseProductDSL {
  def main(args: Array[String]) {

    val productDb:ProductCatalog = ProductDSL.ParseProductFile(args(0))
    val listing:SupplierCatalog = ListingDSL.ParseProductFile(args(1))

    // add each item to the list
    for (item <- listing.getProductList) {
     productDb.addProductListing(item)
    }

    //println(productDb)
    //write to file
    val out = new FileWriter(args(2))
    out.write(productDb.toString)
    out.close

  }
}
