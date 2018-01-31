using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class ControllerScript : MonoBehaviour {

    bool inCube = false;

    GameObject sphere = null;
    GameObject box = null;

    public Vector3 offset;

    public bool broadcasting;
    
    private SteamVR_TrackedObject trackedObj;
    
    private SteamVR_Controller.Device Controller
    {
        get { return SteamVR_Controller.Input((int)trackedObj.index); }
    }

    void Awake()
    {
        trackedObj = GetComponent<SteamVR_TrackedObject>();
    }

    // 1
    public void OnTriggerEnter(Collider other)
    {
        Debug.Log("ENTERED");
        if (!inCube) { 
            HandleEnerBox(other);
        }
    }

    // 2
    public void OnTriggerStay(Collider other)
    {
        if (!inCube) { 
        HandleEnerBox(other);
    }
}

    // 3
    public void OnTriggerExit(Collider other)
    {
        Debug.Log("EXITED");
        if (other.CompareTag("Box") && inCube)
        {
            inCube = false;
        }
    }

    public void HandleEnerBox(Collider other)
    {

        if (other.CompareTag("Box"))
        {
            box = other.gameObject;
            sphere = box.transform.GetChild(0).gameObject;
            inCube = true;
        }

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

                    float xVal = sphereVector.x + .5f;
                    float yVal = sphereVector.y + .5f;
                    float zVal = sphereVector.z + .5f;

                    Debug.Log("Sphere Output Vector -- X:" + xVal + " Y:" + yVal + " Z:" + zVal);
                }
            } else {
                sphere.transform.localPosition = new Vector3(0, 0, 0);
            }
        }
    }
}
