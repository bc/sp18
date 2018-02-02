using UnityEngine;
using System.Collections;
using System.Collections.Generic;
using System.Text;
using System;

public class socketScript : MonoBehaviour {


	private TCPConnection myTCP;
	private string serverMsg;
	public string msgToServer;
	public GameObject leftController; //set this in the inspector
    public GameObject rightController; //set this in the inspector
    private ControllerScript leftControllerScript;
    private ControllerScript rightControllerScript;
    private float time;
    private float timestep = 3;

    // create a TCP connection and get copies of the ControllerScripts when the game starts
    void Awake() {
		//add a copy of TCPConnection to this game object
		myTCP = gameObject.AddComponent<TCPConnection>();
		leftControllerScript = leftController.GetComponent<ControllerScript> ();
        rightControllerScript = rightController.GetComponent<ControllerScript>();
        time = Time.time;
    }
	
    // connect to the server on start
	void Start () {
		myTCP.setupSocket ();
	}
	
    // on update, check for a server response and send data if there's data to send
	void Update() {
        //check for a server response
		SocketResponse ();
		//if connection has not been made, display button to connect
		if (myTCP.socketReady == false) {
			myTCP.setupSocket();
		}
		//once connection has been made, display editable text field with a button to send that string to the server (see function below)
		if (myTCP.socketReady == true && Time.time - time > timestep) {
            string toSend = "";
            //if the left controller has data to send, add it to the string
			if (leftControllerScript.isReady) {
                toSend += leftControllerScript.text;
                toSend += '\n';
                leftControllerScript.isReady = false;
            }
            else
            {
                toSend += "Controller: L Out of Bounds \n";

            }
            //if right controller has data to send, add it to the string
            if (rightControllerScript.isReady)
            {
                toSend += rightControllerScript.text;
                toSend += '\n';
                rightControllerScript.isReady = false;
            } else {
                toSend += "Controller: R Out of Bounds \n";

            }

            //send data
            SendToServer(toSend + "\r\n");
            //send '#' to tell the server we're done sending data
            SendToServer("#");

            time = Time.time;
        }
	}
		
	//socket reading script
	void SocketResponse() {
		string serverSays = myTCP.readSocket();
		if (serverSays != "") {
			Debug.Log("[SERVER]" + serverSays);
		}
	}
		
	//send message to the server
	public void SendToServer(string str) {
		myTCP.writeSocket(str);
		Debug.Log ("[CLIENT] -> " + str);
	}

}
