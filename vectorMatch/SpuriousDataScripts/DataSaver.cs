using System.Collections;
using System.Collections.Generic;
using System.IO;
using System.Text;
using System;
using UnityEngine;

/*
 * 
 * Data Saving File System Archetecture: 
 *              Result
 *                  -SessionX 
 *                      -Config.txt
 *                      -TrialY.txt
 * 
 * Let SessionX stand for whenever the game starts.
 * Let Config be the file that characterizes the human subject. 
 * Let TrialY be every time target is reached. 
 */


public class DataSaver
{
    static string resultsPath;
    static string sessionPath;
    static string configPath;

    static int sessionNum = 0;
    static int trialNum = 0;
    static string sessionPrefix = "session_";

    //Convention uses spaces after ':'
    private static string patientPrefix = "PATIENT_NAME: ";
    private static string datePrefix = "SESSION_START_TIME: ";

    public static void init(string patientName)
    {
        //Sets resultPath val for easy reference to top-level directory
        resultsPath = Path.Combine(Application.persistentDataPath, "result");
        Debug.Log("Results Path: " + resultsPath);
        Debug.Log("DirectoryName: " + Path.GetDirectoryName(resultsPath));


        if (!Directory.Exists(resultsPath))
        {
            Directory.CreateDirectory(resultsPath);
        }

        //Create new session folder
        sessionPath = Path.Combine(resultsPath, sessionPrefix + sessionNum);

        while (Directory.Exists(sessionPath))
        {
            sessionNum++;
            sessionPath = Path.Combine(resultsPath, sessionPrefix + sessionNum);
        }
        Debug.Log("Created Directory: " + sessionPath);

        if (!Directory.Exists(sessionPath))
        {
            Directory.CreateDirectory(sessionPath);
        }

        configPath = Path.Combine(sessionPath, "config.txt");

        Debug.Log(configPath);

        using (StreamWriter sw = File.CreateText(configPath))
        {
            sw.WriteLine(patientPrefix + patientName);

            Int32 UnixTime = (Int32)(DateTime.UtcNow.Subtract(new DateTime(1970, 1, 1))).TotalSeconds;

            sw.WriteLine(datePrefix + UnixTime + "|" + DateTime.Now.ToString("MMMM dd, yyyy"));
        }
    }

    public static void saveTrial<T>(T trialData)
    {
        saveData(trialData, "trial_" + trialNum);
        trialNum++;
    }

    //Save Data
    public static void saveData<T>(T dataToSave, string dataFileName)
    {
        string tempPath = Path.Combine(sessionPath, dataFileName + ".txt");

        //Convert To Json then to bytes
        string jsonData = JsonUtility.ToJson(dataToSave, true);
        byte[] jsonByte = Encoding.ASCII.GetBytes(jsonData);

        //Create Directory if it does not exist
        if (!Directory.Exists(Path.GetDirectoryName(tempPath)))
        {
            Directory.CreateDirectory(Path.GetDirectoryName(tempPath));
        }
        //Debug.Log(path);

        try
        {
            File.WriteAllBytes(tempPath, jsonByte);
            Debug.Log("Saved Data to: " + tempPath.Replace("/", "\\"));
        }
        catch (Exception e)
        {
            Debug.LogWarning("Failed To PlayerInfo Data to: " + tempPath.Replace("/", "\\"));
            Debug.LogWarning("Error: " + e.Message);
        }
    }

    //Load Data
    public static T loadData<T>(string dataFileName)
    {
        string tempPath = Path.Combine(Application.persistentDataPath, "data");
        tempPath = Path.Combine(tempPath, dataFileName + ".txt");

        //Exit if Directory or File does not exist
        if (!Directory.Exists(Path.GetDirectoryName(tempPath)))
        {
            Debug.LogWarning("Directory does not exist");
            return default(T);
        }

        if (!File.Exists(tempPath))
        {
            Debug.Log("File does not exist");
            return default(T);
        }

        //Load saved Json
        byte[] jsonByte = null;
        try
        {
            jsonByte = File.ReadAllBytes(tempPath);
            Debug.Log("Loaded Data from: " + tempPath.Replace("/", "\\"));
        }
        catch (Exception e)
        {
            Debug.LogWarning("Failed To Load Data from: " + tempPath.Replace("/", "\\"));
            Debug.LogWarning("Error: " + e.Message);
        }

        //Convert to json string
        string jsonData = Encoding.ASCII.GetString(jsonByte);

        //Convert to Object
        object resultValue = JsonUtility.FromJson<T>(jsonData);
        return (T)Convert.ChangeType(resultValue, typeof(T));
    }

    public static bool deleteData(string dataFileName)
    {
        bool success = false;

        //Load Data
        string tempPath = Path.Combine(Application.persistentDataPath, "data");
        tempPath = Path.Combine(tempPath, dataFileName + ".txt");

        //Exit if Directory or File does not exist
        if (!Directory.Exists(Path.GetDirectoryName(tempPath)))
        {
            Debug.LogWarning("Directory does not exist");
            return false;
        }

        if (!File.Exists(tempPath))
        {
            Debug.Log("File does not exist");
            return false;
        }

        try
        {
            File.Delete(tempPath);
            Debug.Log("Data deleted from: " + tempPath.Replace("/", "\\"));
            success = true;
        }
        catch (Exception e)
        {
            Debug.LogWarning("Failed To Delete Data: " + e.Message);
        }

        return success;
    }
}