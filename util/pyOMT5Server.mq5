//+------------------------------------------------------------------+
//|                                                 pyOMT5Server.mq5 |
//|                                                  Paulo Rodrigues |
//|                                         https://www.codekraft.co |
//+------------------------------------------------------------------+
#property copyright "Paulo Rodrigues"
#property link      "https://www.codekraft.co"
#property version   "1.00"


#include <Zmq/Zmq.mqh>
#include <Trade\SymbolInfo.mqh>

extern string PROJECT_NAME = "Python Open Metatrader5 Server";
extern string ZEROMQ_PROTOCOL = "tcp";
extern string HOSTNAME = "*";
extern int REP_PORT = 5555;
extern int MILLISECOND_TIMER = 1;  // 1 millisecond

extern string t0 = "--- Trading Parameters ---";
extern int MagicNumber = 123456;

// CREATE ZeroMQ Context
Context context(PROJECT_NAME);

// CREATE ZMQ_REP SOCKET
Socket repSocket(context,ZMQ_REP);

// VARIABLES FOR LATER
uchar myData[];
ZmqMsg request;


//+------------------------------------------------------------------+
//| Expert initialization function                                   |
//+------------------------------------------------------------------+
int OnInit()
{
    EventSetMillisecondTimer(MILLISECOND_TIMER);     // Set Millisecond Timer to get client socket input

    Print("[REP] Binding MT5 Server to Socket on Port " + IntegerToString(REP_PORT) + "..");

    repSocket.bind(StringFormat("%s://%s:%d", ZEROMQ_PROTOCOL, HOSTNAME, REP_PORT));

    /*
        Maximum amount of time in milliseconds that the thread will try to send messages 
        after its socket has been closed (the default value of -1 means to linger forever):
    */

    repSocket.setLinger(1000);  // 1000 milliseconds

    /* 
      If we initiate socket.send() without having a corresponding socket draining the queue, 
      we'll eat up memory as the socket just keeps enqueueing messages.
      
      So how many messages do we want ZeroMQ to buffer in RAM before blocking the socket?
    */

    repSocket.setSendHighWaterMark(5);     // 5 messages only.

    return(INIT_SUCCEEDED);
}
  
//+------------------------------------------------------------------+
//| Expert deinitialization function                                 |
//+------------------------------------------------------------------+
void OnDeinit(const int reason)
{
    Print("[REP] Unbinding MT5 Server from Socket on Port " + IntegerToString(REP_PORT) + "..");
    repSocket.unbind(StringFormat("%s://%s:%d", ZEROMQ_PROTOCOL, HOSTNAME, REP_PORT));
}
//+------------------------------------------------------------------+
//| Expert timer function                                            |
//+------------------------------------------------------------------+
void OnTimer()
{   
    // Get client's response, but don't wait.
    repSocket.recv(request,true);
    
    // MessageHandler() should go here.   
    MessageHandler(request);
}
//+------------------------------------------------------------------+

void MessageHandler(ZmqMsg &localRequest)
{
    // Output object
    ZmqMsg reply;
    
    // Message components for later.
    string components[];
    
    if(localRequest.size() > 0) {
        // Get data from request   
        ArrayResize(myData, localRequest.size());
        localRequest.getData(myData);
        string dataStr = CharArrayToString(myData);
        
        // Process data
        ParseZmqMessage(dataStr, components);
        
        // Interpret data
        InterpretZmqMessage(components);
    }
}

//+------------------------------------------------------------------+
ENUM_TIMEFRAMES TFMigrate(int tf)
{
    switch(tf)
    {
        case 0: return(PERIOD_CURRENT);
        case 1: return(PERIOD_M1);
        case 5: return(PERIOD_M5);
        case 15: return(PERIOD_M15);
        case 30: return(PERIOD_M30);
        case 60: return(PERIOD_H1);
        case 1440: return(PERIOD_D1);
        case 10080: return(PERIOD_W1);
        case 43200: return(PERIOD_MN1);
        
        default: return(PERIOD_CURRENT);
    }
}

//+------------------------------------------------------------------+
// Interpret Zmq Message and perform actions
void InterpretZmqMessage(string& compArray[])
{
    Print("ZMQ: Interpreting Message..");


    int switch_action = 0;
    string volume;


    if (compArray[0] == "DATA")
        switch_action = 1;
        
    string ret = "";
    int ticket = -1;
    bool ans = false;

    MqlRates rates[];
    ArraySetAsSeries(rates, true);    

    int price_count = 0;
    
    ZmqMsg msg("[SERVER] Processing");
    
    switch(switch_action) 
    {
        case 1:
            ret = "";
            
            // Format: DATA|SYMBOL|TIMEFRAME|START_DATETIME|END_DATETIME
            price_count = CopyRates(compArray[1], TFMigrate(StringToInteger(compArray[2])),
                          StringToTime(compArray[3]), StringToTime(compArray[4]),
                          rates);
            
            if (price_count > 0)
            {              
                // Construct string of price|price|price|.. etc and send to PULL client.
                for(int i = 0; i < price_count; i++ ) {                        
                      ret = ret + StringFormat("%s, %.4f,%.4f,%.4f,%.4f,%d,%d%s", TimeToString(rates[i].time), rates[i].open, rates[i].low, rates[i].high, rates[i].close, rates[i].tick_volume, rates[i].real_volume, "|");
                }
              
                repSocket.send(ret, false);
            } else {
               repSocket.send("NO DATA", false);
            }
            
            break;
        default: 
            break;
    }
}
//+------------------------------------------------------------------+
// Parse Zmq Message
void ParseZmqMessage(string& message, string& retArray[]) 
{   
    Print("Parsing: " + message);
    
    string sep = "|";
    ushort u_sep = StringGetCharacter(sep,0);
    
    int splits = StringSplit(message, u_sep, retArray);
    
    for(int i = 0; i < splits; i++) {
        Print(IntegerToString(i) + ") " + retArray[i]);
    }
}
