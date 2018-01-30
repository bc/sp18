using UnityEngine;

public class socketScript : MonoBehaviour
{ //variables 
    private TCPConnection myTCP;
    private string serverMsg;
    public string msgToServer;

    void Awake()
    {

        myTCP = gameObject.AddComponent<TCPConnection>();
        Connect();
    }


    void Update()
    {
        //keep checking the server for messages, if a message is received from server, it gets logged in the Debug console (see function below) 

        SocketResponse();

    }

    private void Connect()
    {
        //if connection has not been made, display button to connect 
        if (myTCP.socketReady == false)
        {
            //try to connect 
            Debug.Log("Attempting to connect..");
            myTCP.setupSocket();
        }


        //once connection has been made, display editable text field with a button to send that string to the server (see function below) 
        if (myTCP.socketReady == true)
        {
            msgToServer = "Connection Successful";
            SendToServer(msgToServer);
        }

    }

    //socket reading script 
    void SocketResponse()
    {
        //string serverSays = myTCP.readSocket();
        /*if (serverSays != "") {
            Debug.Log("[SERVER]" + serverSays);
        }*/
    }

    //send message to the server 
    public void SendToServer(string str)
    {
        myTCP.writeSocket(str);
        Debug.Log("[CLIENT] -> " + str);
    }
}


/*public class SocketScript : MonoBehaviour {

// Use this for initialization
void Start () {

}

// Update is called once per frame
void Update () {

}*/

//}