using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class CenterTarget : MonoBehaviour
{

    //public OutputSphere output;
    Vector3 selectionPoint;
    public bool selected = false;

    // Use this for initialization
    void Start()
    {
        this.gameObject.SetActive(false);
    }

    private void OnTriggerEnter(Collider other)
    {
        if (other.CompareTag("OutputSphere"))
        {
            selected = true;
        }
    }

    private void OnTriggerStay(Collider other)
    {
        if (other.CompareTag("OutputSphere"))
        {
            selected = true;
        }
    }

    private void OnTriggerExit(Collider other)
    {
        if (other.CompareTag("OutputSphere"))
        {
            selected = false;
        }
    }

    // Update is called once per frame
    void Update()
    {

    }

    public void setPosition(Vector3 pos)
    {
        Debug.Log(pos.ToString());
        if (!gameObject.activeSelf) gameObject.SetActive(true);
        this.gameObject.transform.localPosition = pos;
    }
}