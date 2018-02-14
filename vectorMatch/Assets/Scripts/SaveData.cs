using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using UnityEditor;
using System.IO;

public class SaveData : MonoBehaviour {

	public List<string> data;
	public GameObject leftController; //set this in the inspector
	public GameObject rightController; //set this in the inspector
	private ControllerScript leftControllerScript;
	private ControllerScript rightControllerScript;
	private int updateCount;
	private int saveSize = 1800;
	private StreamWriter writer;
	private string path = "Assets/SaveData/data.txt";

	// Use this for initialization
	void Start () {
		leftControllerScript = leftController.GetComponent<ControllerScript> ();
		rightControllerScript = rightController.GetComponent<ControllerScript>();
		updateCount = 0;
        File.WriteAllText(path, string.Empty);
		writer = new StreamWriter(path, true);
	}
	
	// Update is called once per frame
	void Update () {
		data.Add (rightControllerScript.text);
		data.Add (leftControllerScript.text);

		if (updateCount >= saveSize) {
            string output = "";
            foreach (var line in data) {
                output += line + "\n\n";
            }
            WriteToFile(output);
            updateCount = 0;
		}

        updateCount++;
	}

	void WriteToFile(string data)
	{
        //Write some text to the test.txt file
        Debug.Log(data);
		writer.WriteLine(data);

		//Re-import the file to update the reference in the editor
		//AssetDatabase.ImportAsset(path); 
		//TextAsset asset = Resources.Load("data");

		//Print the text from the file
		Debug.Log("Autosaved");
	}

	void OnApplicationQuit() {
		writer.Close();
	}
}
