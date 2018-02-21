using System.Collections;
using System.Collections.Generic;
using UnityEngine;


public class TargetBallScript : MonoBehaviour {

    public ControllerScript controller;
    Vector3 selectionPoint;
    public bool selected = false;

	// Use this for initialization
	void Start () {
        this.gameObject.SetActive(false);
    }

    private void OnTriggerEnter(Collider other)
    {
        if (other.CompareTag("Controller"))
        {
            selected = true;
        }
    }

    private void OnTriggerStay(Collider other)
    {
        if (other.CompareTag("Controller"))
        {
            selected = true;
        }
    }

    private void OnTriggerExit(Collider other)
    {
        if (other.CompareTag("Controller"))
        {
            selected = false;
        }
    }

    // Update is called once per frame
    void Update () {

	}

    public void setPosition(Vector3 pos)
    {
        if (!gameObject.activeSelf) gameObject.SetActive(true);
        this.gameObject.transform.localPosition = pos;
    }
}
