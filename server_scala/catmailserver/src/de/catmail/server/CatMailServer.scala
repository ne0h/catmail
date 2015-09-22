package de.catmail.server

import de.catmail.api.CatMailService

import com.typesafe.config.ConfigFactory

import org.apache.thrift.protocol.TBinaryProtocol
import org.apache.thrift.server.TThreadPoolServer
import org.apache.thrift.transport.TFramedTransport
import org.apache.thrift.transport.TServerSocket

/**
 * @author ne0h
 */
object CatMailServer {
	
	def start() {
		val conf = ConfigFactory.load
		
		println("Starting server...")
		
		val handler = new CatMailServerHandler()
		val processor = new CatMailService.Processor[CatMailServerHandler](handler)
		
		try {
			val serverTransport = new TServerSocket(conf.getInt("server.port"))
			
			val serverArgs: TThreadPoolServer.Args = new TThreadPoolServer.Args(serverTransport)
			serverArgs.transportFactory(new TFramedTransport.Factory())
			serverArgs.protocolFactory(new TBinaryProtocol.Factory(true, true))
			
			new TThreadPoolServer(serverArgs).serve
		} catch {
			case e: Exception => e.printStackTrace() 
		}
		
		println("Server started.")
	}
	
	def main(args: Array[String]) {
		CatMailServer.start
	}
	
}