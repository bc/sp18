using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class MatrixMultiplication : MonoBehaviour {

    public GameObject leftController; //set this in the inspector
    public GameObject rightController; //set this in the inspector
    private ControllerScript leftControllerScript;
    private ControllerScript rightControllerScript;
    private double[,] controllerCoordinates;
    private double[,] hand3_ultraflex;
    private double[,] hand4_ultraflex;
    private double[,] identity;
    private double[,] transformMatrix;
    private double[] scale;
    private double[] mins;
    private Vector3 result;
    public GameObject box;
    private GameObject sphere;
    public bool isHand3;
    public bool isHand4;
    public bool isIdentity;
    public bool matrixChanged;

    // Use this for initialization
    void Start()
    {
        isHand3 = true;
        matrixChanged = false;
        leftControllerScript = leftController.GetComponent<ControllerScript>();
        rightControllerScript = rightController.GetComponent<ControllerScript>();
        sphere = box.transform.GetChild(0).gameObject;
        controllerCoordinates = new double[1, 7];
        controllerCoordinates[0, 6] = 0;
        hand3_ultraflex = new double[7, 6] {
            { 0.08848152, 0.005962941, 0.14381746, 1.217437e-03, -0.003103362, -0.0001697737 },
            { 0.09123613, -0.006078463,  0.17772115, -6.700282e-05, -0.003325758, -0.0002302716},
            { -0.03392852, -0.025141921, -0.18999517, -4.953349e-03,  0.002157888, 0.0002234035},
            { 0.06026345,  0.024543637, -0.42907164, -4.036174e-03,  0.001247087, 0.0011713661},
            { 0.14890032,  0.068994323, -0.38542170,  4.236988e-03, -0.001949607, 0.0005531862},
            { -0.19059219,  0.055208703, -0.17218006,  4.712386e-03,  0.005874256, 0.0010128159},
            { -0.17197715,  0.049936650,  0.01661992,  3.884230e-03,  0.003561464, 0.0009869429}
        };

        //X: (-0.225,0.3888)

        identity = new double[7, 6] { 
            {1, 0, 0, 0, 0, 0},
            {0, 1, 0, 0, 0, 0},
            {0, 0, 1, 0, 0, 0},
            {0, 0, 0, 1, 0, 0},
            {0, 0, 0, 0, 1, 0},
            {0, 0, 0, 0, 0, 1},
            {0, 0, 0, 0, 0, 0}
        };

        hand4_ultraflex = new double[7, 6] 
        { 
            { 0.039516170, -0.0028948473, 0.08718748, 0.0001413771, -1.091838e-03, -2.037809e-04 },
            {  0.002908213, -0.0061843186,  0.03988505, -0.0002079789, -3.107123e-05, -1.844063e-04},
            { -0.157048530, -0.0403979750,  0.02311287, -0.0023261392,  4.627887e-03, -4.393248e-04},
            { -0.199904950,  0.0007397363, -0.13808078,  0.0009649270,  7.031483e-03,  2.458143e-04},
            { -0.148416545,  0.0083718367, -0.15459901,  0.0033855050,  5.620852e-03, -2.938439e-04},
            { -0.161303554, -0.0016516848, -0.25434879,  0.0001118287,  6.032746e-03, -7.924072e-06},
            { -0.119837390,  0.0264979731, -0.01599160,  0.0019460272,  1.956893e-03,  6.493364e-04}
        };



        transformMatrix = hand3_ultraflex;
        scale = new double[3];
        mins = new double[3];
        setScale();
    }

    // Update is called once per frame
    void Update () {
        if (Input.GetKeyDown(KeyCode.Space)) {
            if (isHand3)
            {
                transformMatrix = hand4_ultraflex;
                isHand3 = false;
                isHand4 = true;
                setScale();
                Debug.Log("transformMatrix is hand4");
            }
            else if (isHand4)
            {
                transformMatrix = identity;
                isHand4 = false;
                isIdentity = true;
                setScale();
                Debug.Log("transformMatrix is identity");
            }
            else if (isIdentity)
            {
                transformMatrix = hand3_ultraflex;
                isHand3 = true;
                isIdentity = false;
                setScale();
                Debug.Log("transformMatrix is hand3");
            }

            matrixChanged = true;
        }
        Vector3 left = leftControllerScript.coordinates;
        Vector3 right = rightControllerScript.coordinates;
        controllerCoordinates[0,0] = left.x;
        controllerCoordinates[0,1] = left.y;
        controllerCoordinates[0,2] = left.z;
        controllerCoordinates[0,3] = right.x;
        controllerCoordinates[0,4] = right.y;
        controllerCoordinates[0,5] = right.z;
        setOutputSphereCoordinates();
        sphere.transform.localPosition = result;

    }

    void setOutputSphereCoordinates()
    {
        result = matrixMultiply(controllerCoordinates, transformMatrix);
        //result.x *= (float)scale[0];
        //result.y *= (float)scale[1];
        //result.z *= (float)scale[2];
        result.x = (result.x - (float)mins[0]) * (float)scale[0] * 4 - 0.5f * box.transform.localScale.x * 4;
        result.y = (result.y - (float)mins[1]) * (float)scale[1] * 4 - 0.5f * box.transform.localScale.x * 4;
        result.z = (result.z - (float)mins[2]) * (float)scale[2] * 4 - 0.5f * box.transform.localScale.x * 4;
    }

    public Vector3 getTargetLocation(double[,] coord)
    {
        Vector3 newLoc = matrixMultiply(coord, transformMatrix);
        //newLoc.x *= (float)scale[0];
        //newLoc.y *= (float)scale[1];
        //newLoc.z *= (float)scale[2];
        newLoc.x = (newLoc.x - (float)mins[0]) * ((float)scale[0] * 4) - 0.5f * box.transform.localScale.x * 4;
        newLoc.y = (newLoc.y - (float)mins[1]) * ((float)scale[1] * 4) - 0.5f * box.transform.localScale.x * 4;
        newLoc.z = (newLoc.z - (float)mins[2]) * ((float)scale[2] * 4) - 0.5f * box.transform.localScale.x * 4;
        return newLoc;
    }

    public bool getIsHand3()
    {
        return isHand3;
    }

    private Vector3 matrixMultiply(double[,] a, double[,] b)
    {
        int m = a.GetLength(0);
        int n = b.GetLength(1);
        int o = b.GetLength(0);
        double[,] c = new double[m, n];
        for (int i = 0; i < m; i++)
        {
            for (int j = 0; j < n; j++)
            {
                c[i, j] = 0;
                for (int k = 0; k < o; k++)
                {
                    c[i, j] += a[i, k] * b[k, j];

                }
            }
        }
        Vector3 resultVector = new Vector3((float)c[0, 0], (float)c[0, 1], (float)c[0, 2]);
        return resultVector;
    }

    private void setScale()
    {
        for (int i = 0; i < 3; i++)
        {
            double max = 0;
            double min = 0;
            for (int j = 0; j < 6; j++)
            {
                if (transformMatrix[j, i] > 0)
                {
                    max += transformMatrix[j, i];
                }
                else
                {
                    min += transformMatrix[j, i];
                }
            }
            scale[i] = box.transform.localScale.x / (max - min);
            mins[i] = min;
            Debug.Log(scale[i]);
            //3/4
            //    (value + min) * width/range - 0.5width
        }
    }

    public double[,] getControllerLocation()
    {
        return controllerCoordinates;
    }
}


