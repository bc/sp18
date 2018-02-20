using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class OutputSphere : MonoBehaviour
{
    
    public GameObject target;
    private CenterTarget targetScript;
    public GameObject matrix;
    private MatrixMultiplication matrixScript;
    bool initialized = false;
    private int trialCounter = 0;
    public DSObjectScript dso;
    private float minRand;
    private float maxRand;

    // Use this for initialization
    void Start()
    {
        targetScript = target.GetComponent<CenterTarget>();
        matrixScript = matrix.GetComponent<MatrixMultiplication>();
        minRand = 0.1f;
        maxRand = 0.9f;
        //setNewBallLocations();
        trialCounter = 0;
    }

    // Update is called once per frame
    void Update()
    {
        if (!initialized)
        {
            setNewBallLocations();
            initialized = true;
        }
        if (targetScript.selected)
        {
            dso.info.trialNum = trialCounter;
            DataSaver.saveTrial<TrialInfo>(dso.info);
            dso.info = new TrialInfo();
            ++trialCounter;
            Debug.Log("trials completed: " + trialCounter);
            setNewBallLocations();
        }
        if (matrixScript.matrixChanged)
        {
            setNewBallLocations();
            matrixScript.matrixChanged = false;
        }
    }

    void setNewBallLocations()
    {
        double[,] controllerCoordinates = new double[1, 7] { {Random.Range(minRand, maxRand), Random.Range(minRand, maxRand),
            Random.Range(minRand, maxRand), Random.Range(minRand, maxRand), Random.Range(minRand, maxRand), Random.Range(minRand, maxRand), 0 } };
        Debug.Log(controllerCoordinates[0,0] + " " + controllerCoordinates[0, 1] + " " + controllerCoordinates[0, 2] + " " + 
            controllerCoordinates[0, 3] + " " + controllerCoordinates[0,4] + " " + controllerCoordinates[0, 5]);
        targetScript.setPosition(matrixScript.getTargetLocation(controllerCoordinates));
        Debug.Log("New Loc");
    }
}
