import UnityEngine;
import System.IO;
//import 
#pragma strict

public var fps : float;
private var _svPath : String;
_svPath = "D:/Unity  Programs/something/Assets/pics/";
var picCounter : int;
picCounter = 0;
var cam: WebCamTexture; 
cam = new WebCamTexture();
var time : float; 
time = 0;
var startTime : float;
var snap : Texture2D;

function Start () {
	yield Application.RequestUserAuthorization (UserAuthorization.WebCam | UserAuthorization.Microphone);

	if (Application.HasUserAuthorization(UserAuthorization.WebCam | UserAuthorization.Microphone))
	{
		var devices: WebCamDevice[] = WebCamTexture.devices;
		var numofcams : int = devices.Length;
		//Debug.Log("device0: " + devices[0].name + " device1: " + devices[1].name);
		var i : int;
		for (i = 0; i < numofcams; i++){
			if(devices[i].name == "SplitCam Video Driver"){
				cam.deviceName = devices[0].name;
			}
		}
		cam.requestedFPS = fps;
		var render: Renderer = GetComponent.<Renderer>();
		render.material.mainTexture = cam;
		cam.Play();
		startTime = 0;
	}
	
 	snap = new Texture2D(cam.width, cam.height);
}
function Shots()
 {
 	if(cam.isPlaying && picCounter < 30) {
 	/*	if(picCounter == 0){
 			startTime = Time.time;
 		}*/
 		
 		snap.SetPixels(cam.GetPixels());
 		snap.Apply();
	
		//var bytes : byte[];
		//bytes = snap.EncodeToPNG();
	/*
		var fileSave : FileStream;
		fileSave = new FileStream(_svPath+picCounter.ToString() + ".png", FileMode.Create);
	
		var binary : BinaryWriter;
		binary = new BinaryWriter(fileSave);
    	binary.Write(bytes);
    	fileSave.Close();
		++picCounter;*/
	 }	
	 if(picCounter == 30){
	 	//Debug.Log((Time.time - startTime).ToString());
	 	++picCounter;
	}
 } 
function Update () {
	
	//if (Time.time > time + 1/20) {
	//	time = Time.time;
		Shots();
	
	//}
	
}
