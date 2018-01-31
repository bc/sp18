using UnityEngine;
using System.Collections;
using System.Collections.Generic;
using System.Text;
using System;

public class socketScript : MonoBehaviour {

	private TCPConnection myTCP;
	private string serverMsg;
	public string msgToServer;
	public GameObject player; //must set player in the inspector
	private PlayerController playerController;

	void Awake() {
		//add a copy of TCPConnection to this game object
		myTCP = gameObject.AddComponent<TCPConnection>();
		playerController = player.GetComponent<PlayerController> ();
	}
		
	void Start () {
		myTCP.setupSocket ();
	}
		
	void Update() {
		SocketResponse ();
		//if connection has not been made, display button to connect
		if (myTCP.socketReady == false) {
			myTCP.setupSocket();
		}
		//once connection has been made, display editable text field with a button to send that string to the server (see function below)
		if (myTCP.socketReady == true) {
			if (playerController.isReady) {
				SendToServer(playerController.text);
				playerController.isReady = false;
			}
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
