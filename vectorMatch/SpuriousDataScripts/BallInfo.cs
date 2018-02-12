using System;
using System.Collections;
using System.Collections.Generic;
using UnityEngine;

[System.Serializable]
public class BallInfo
{
    public List<float> x = new List<float>();
    public List<float> z = new List<float>();
    public List<Int64> timeStamp = new List<Int64>();
    public int count;
}
