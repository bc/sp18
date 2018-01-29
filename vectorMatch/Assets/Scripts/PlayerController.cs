using System.Collections;
using System.Collections.Generic;
using UnityEngine;
public class PlayerController : MonoBehaviour
{
    private Rigidbody rb;
    public float amplifier;
    private Vector3 nextPosition;
    private socketScript ss;
    

    void Start()
    {
        ss = gameObject.AddComponent<socketScript>();
    }

    void Update()
    {
        rb = GetComponent<Rigidbody>();

    }
    void FixedUpdate()
    {
        //float xPos = leftController.transform.position.x;
        //float moveHorizontal = Input.GetAxis("Horizontal");
        //float moveVertical = Input.GetAxis("Vertical");
        //Vector3 movement = new Vector3(moveHorizontal, 0.0f, moveVertical);
        //if (leftDevice.GetHairTrigger())
        //{
        //    rb.transform.position = leftController.transform.position * amplifier;
        //} else
        //{
        //    rb.transform.position = leftController.transform.position * 2;
        //}
    }
    void OnTriggerEnter(Collider other)
    {
        if (other.gameObject.CompareTag("Pick Up"))
        {
            Vector3 randomPosition = new Vector3(Random.Range(-10.0f, 10.0f), 0.5f, Random.Range(-10.0f, 10.0f));
            other.gameObject.transform.position = randomPosition;

            // send the data here
            string pos = randomPosition.x.ToString() + "," + randomPosition.y.ToString() + "," + randomPosition.z.ToString();

            ss.SendToServer(pos);
        }
    }
}