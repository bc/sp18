using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class LeftControllerScript : MonoBehaviour {
    
    public GameObject model;
    public GameObject controlledObject;
    public int amp;

    // 1
    private SteamVR_TrackedObject trackedObj;
    // 2
    private SteamVR_Controller.Device Controller
    {
        get { return SteamVR_Controller.Input((int)trackedObj.index); }
    }

    void Awake()
    {
        trackedObj = GetComponent<SteamVR_TrackedObject>();
    }

    // Update is called once per frame
    void Update () {

        if (Controller.GetHairTrigger())
        {
            Debug.Log(gameObject.name + " Trigger Press");
            if (controlledObject != null)
                controlledObject.transform.position = new Vector3(model.transform.position.x * amp, controlledObject.transform.position.y, model.transform.position.z * amp);
        } else
        {
            if (controlledObject != null)
                controlledObject.transform.position = new Vector3(model.transform.position.x * 2, controlledObject.transform.position.y, model.transform.position.z * 2);
        } 

        float xVal = model.transform.position.x;
        float yVal = model.transform.position.y;
        float zVal = model.transform.position.z;


        Debug.Log("Position: X: " + xVal + " Y: " + yVal + " Z: " +zVal);
    }
}
