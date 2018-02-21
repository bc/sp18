using System.Collections;
using System.Collections.Generic;
using System;
using UnityEngine;

public class DSObjectScript : MonoBehaviour {

    public string patientName;
    public GameObject RController;
    public GameObject LController;
    public GameObject targetBall;
    public GameObject outputBall;
    public GameObject matrixObject;
    MatrixMultiplication matrixScript;
    public bool RECORDING;

    public TrialInfo info;

    private void Awake()
    {
        DataSaver.init(this.patientName);
        info = new TrialInfo();
        matrixScript = matrixObject.GetComponent<MatrixMultiplication>();
    }

    // Use this for initialization
    void Start () {
		
	}
	
	// Update is called once per frame
	void Update () {
        info.timestamp.Add((Int64)(DateTime.UtcNow.Subtract(new DateTime(1970, 1, 1))).TotalMilliseconds);

        info.rightPosition.Add(RController.transform.localPosition);
        info.leftPosition.Add(LController.transform.localPosition);

        info.rightEuler.Add(RController.transform.localEulerAngles);
        info.leftEuler.Add(LController.transform.localEulerAngles);

        info.outputPosition.Add(outputBall.transform.localPosition);

        info.targetPosition = targetBall.transform.localPosition;

        info.targetPosition = targetBall.transform.localPosition;

        if (matrixScript.getIsHand3())
        {
            info.handType = "hand3";
        } else
        {
            info.handType = "hand4";
        }


    }
}
