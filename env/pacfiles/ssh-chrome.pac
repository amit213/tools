
//
// Define the network paths (direct, proxy and deny)
//

// Default connection
var direct = "DIRECT";

// Proxy Server
//var proxy = "SOCKS5 127.0.0.1:2015;";
var proxy = "SOCKS5 127.0.0.1:15015;";

// Default localhost for denied connections
var deny = "SOCKS5 127.0.0.1:65535";

//
// Proxy Logic
//

function FindProxyForURL(url, host)
{
   
   //return deny;
   return proxy; 


      if ( shExpMatch(url, "*google*") )
        { return deny;}
      if ( shExpMatch(url, "*facebook*") ) 
        { return deny;}
      if ( shExpMatch(url, "*outlook*") ) 
        { return deny;}


   //return deny;
   return proxy; 
}
