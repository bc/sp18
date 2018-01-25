using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class CameraController : MonoBehaviour {
	public GameObject player;
	private Vector3 offset;
	// Use this for initialization
	void Start () {
		offset = transform.position - player.transform.position;
	}
	
	// Update is called once per frame
	// late update runs every frame, but runs at the end. good for cameras/ the last layer of operations. 
	void LateUpdate () {
		transform.position = player.transform.position + offset;
	}
}
