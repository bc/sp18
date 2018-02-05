using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class TargetControllerScript : MonoBehaviour {

    public GameObject lBall;
    public GameObject rBall;

    TargetBallScript lBallScript;
    TargetBallScript rBallScript;


    // Use this for initialization
    void Start () {
        lBallScript = lBall.GetComponent<TargetBallScript>();
        rBallScript = rBall.GetComponent<TargetBallScript>();
        setNewBallLocations();
	}
	
	// Update is called once per frame
	void Update () {
		if(lBallScript.selected && rBallScript.selected)
        {
            setNewBallLocations();
        }
	}

    void setNewBallLocations()
    {
        lBallScript.setPosition(new Vector3(Random.Range(-.5f, .5f), Random.Range(-.5f,.5f),Random.Range(-.5f,.5f)));
        rBallScript.setPosition(new Vector3(Random.Range(-.5f, .5f), Random.Range(-.5f, .5f), Random.Range(-.5f, .5f)));
    }
}
