﻿using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class ControllerScript : MonoBehaviour {

    //True if controller is in cube
    bool inCube = false;

    //Holders for sphere and box
    GameObject sphere = null;
    GameObject box = null;

    //Offset to make the ball appear in a nice location relative to the controller.
    public Vector3 offset;

    //Are we currently transmitting the data from this device?
    public bool broadcasting;
    
    //Network objects
    public bool isReady = false;
    public string text;
    
    //SteamVR boiler plate
    private SteamVR_TrackedObject trackedObj;
    private SteamVR_Controller.Device Controller
    {
        get { return SteamVR_Controller.Input((int)trackedObj.index); }
    }

    void Awake()
    {
        trackedObj = GetComponent<SteamVR_TrackedObject>();
    }

    // When the controller (gameObject that owns the script) enters a trigger, it sends a debug message,
    // and if it's a box
    public void OnTriggerEnter(Collider other) {
        Debug.Log("ENTERED");
        if (!inCube && other.CompareTag("Box")) { 
            HandleEnterBox(other);
        }
    }

    // Just handles debouncing, really. In other words, keeps the values from flip-flopping at the right time.
    public void OnTriggerStay(Collider other)
    {
        if (!inCube && other.CompareTag("Box")) { 
        HandleEnterBox(other);
        }
    }

    // When the controller leaves an object and that object is the box, set the state of the box to false.
    public void OnTriggerExit(Collider other)
    {
        Debug.Log("EXITED");
        if (other.CompareTag("Box") && inCube)
        {
            inCube = false;
        }
    }

    // Handles state transition upon entering ONLY THE BOX. Does not check if object is box.
    public void HandleEnterBox(Collider other)
    {
        box = other.gameObject;
        sphere = box.transform.GetChild(0).gameObject;
        inCube = true;

    }

    // Update is called once per frame
    void Update () { 

        //If we've seen a sphere
        if(sphere)
        {
            //potential location of the sphere IFF it stays within the cube;
            Vector3 potentialSphereLoc = gameObject.transform.position + gameObject.transform.TransformVector(offset);

            //if we're in a  cube, then set the location of the sphere we've seen to the location of the inside of the ring of the vive.
            // Otherwise, set the location of the sphere to the origin point of the given cube.
            if (inCube && box.GetComponent<MeshFilter>().mesh.bounds.Contains(sphere.GetComponent<MeshFilter>().mesh.bounds.center))
            {
                sphere.transform.position = potentialSphereLoc;
                if (broadcasting)
                {
                    Vector3 sphereVector = sphere.transform.localPosition;
                    Vector3 boxSize = box.GetComponent<BoxCollider>().bounds.size;

                    //Holds L or R if controller is left or right.
                    char cVal;

                    if (gameObject.name.Contains("left"))
                    {
                        cVal = 'L';
                    } else
                    {
                        cVal = 'R';
                    }

                    //Corrected 3D space variables relative to the internal sphere.
                    // Coordinate space is from 0,0,0 in bottom front left, to 1,1,1 in top back right.
                    float xVal = sphereVector.x + .5f;
                    float yVal = sphereVector.y + .5f;
                    float zVal = sphereVector.z + .5f;

                    text = "Controller: " + cVal + " X:" + xVal + " Y:" + yVal + " Z:" + zVal;
                    isReady = true;
                    //Debug.Log(text);
                }
            } else {
                //If we're not in the cube, don't say we're ready, and set the ball back back to the center of the cube.
                sphere.transform.localPosition = new Vector3(0, 0, 0);
                isReady = false;
            }
        }
    }

    public Vector3 getSelectionPoint()
    {
        return gameObject.transform.position + gameObject.transform.TransformVector(offset);
    }
}
