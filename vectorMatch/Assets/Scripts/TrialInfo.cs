using System.Collections;
using System.Collections.Generic;
using System;
using UnityEngine;
[System.Serializable]
public class TrialInfo {
    public List<Int64> timestamp = new List<Int64>();

    public List<Vector3> rightPosition = new List<Vector3>();
    public List<Vector3> leftPosition = new List<Vector3>();

    public List<Vector3> rightEuler = new List<Vector3>();
    public List<Vector3> leftEuler = new List<Vector3>();

    public Vector3 targetPosition = new Vector3();
    public List<Vector3> outputPosition = new List<Vector3>();

    public string handType = "ERR";
    public int trialNum = 0;
}
