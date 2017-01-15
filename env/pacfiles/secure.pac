
//
// Define the network paths (direct, proxy and deny)
//

// Default connection
var direct = "DIRECT";

// Proxy Server
//var proxy = "SOCKS5 127.0.0.1:2015;";
var proxy = "SOCKS5 127.0.0.1:9150;";
//var proxy = "DIRECT";

// Default localhost for denied connections
var deny = "SOCKS5 127.0.0.1:65535";

//
// Proxy Logic
//

function FindProxyForURL(url, host)
{
      //if ( shExpMatch(url, "*icanhazip/*") ) 

      if ( shExpMatch(url, "*lendingclub*") )
        { return deny;}
      if ( shExpMatch(url, "*mysigmahomenas*") )
        { return deny;}
      if ( shExpMatch(url, "*gmail*") )
        { return deny;}
      //if ( shExpMatch(url, "*google.com*") )
      //  { return deny;}
      if ( shExpMatch(url, "*facebook*") ) 
        { return deny;}
      if ( shExpMatch(url, "*outlook*") ) 
        { return deny;}


   //return deny;
   return proxy; 
}
