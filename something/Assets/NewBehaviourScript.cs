using UnityEngine;
using System.Collections;
using System.Net.Sockets;
using System.Net;
using System.IO;
using System.Text;
using System;



public class NewBehaviourScript : MonoBehaviour {

	public GameObject eye1;
	public GameObject eye2;
	public Stream stream;
	Byte[] data = new Byte[256];
	Int32 bytes = 0;
	String responseData = String.Empty;
	Char[] splits;
	String[] mystring;
	Byte[] checkstring = new Byte[256];
	float foo, bar, jss;
	float oldeyex, oldeyey;
	Boolean changed;
	// Use this for initialization
	void Start () {
		//eye1 = GameObject.Find("eye1");
		//eye2 = GameObject.Find("eye2");
		//Debug.Log(eye1.transform.position.ToString ());
		splits = new Char[] {'(',',',')',' '};
		stream = Connect ("127.0.0.1", "begin", data);
		checkstring = System.Text.Encoding.ASCII.GetBytes("good\r\n");
	}
	
	// Update is called once per frame
	void Update () {

		if (stream == null) {
			return;
		}


		bytes = stream.Read (data, 0, data.Length);
		if (responseData != System.Text.Encoding.ASCII.GetString (data, 0, bytes)) {
			changed = true;
			oldeyex = eye1.transform.position.x;
			oldeyey = eye1.transform.position.y;
		}
		responseData = System.Text.Encoding.ASCII.GetString (data, 0, bytes);

		//Debug.Log(responseData.ToString());
		//Debug.Log ("\n");
		mystring = responseData.Split(splits);
		Debug.Log(mystring[13].ToString());
		stream.Write(checkstring, 0, checkstring.Length);
		foo = float.Parse (mystring [4].ToString ());
		jss = foo - 120;
		foo = foo - 2 * jss;
		bar = float.Parse (mystring [10].ToString ());
		jss = bar - 120;
		bar = bar - 2 * jss;
		if (changed == true) {
			oldeyex = oldeyex - float.Parse (mystring[2].ToString ());
			oldeyey = oldeyey - foo;
			oldeyex = (float) Math.Sqrt (Math.Pow(oldeyex,2) + Math.Pow (oldeyey,2));
			Debug.Log (oldeyex);
		}
		eye1.transform.Translate(-(eye1.transform.position.x + float.Parse(mystring[2].ToString())),-(eye1.transform.position.y - foo),0);
		eye2.transform.Translate(-(eye2.transform.position.x + float.Parse(mystring[8].ToString())),-(eye2.transform.position.y - bar),0);
		eye1.transform.rotation = Quaternion.Slerp(eye1.transform.rotation, Quaternion.Euler(0,57.295779f*float.Parse(mystring[13].ToString()),0), Time.deltaTime*3.0f);
		changed = false;
	}

	static Stream Connect(String server, String message, Byte[] data) 
	{

		try {
				// Create a TcpClient.
				// Note, for this client to work you need to have a TcpServer 
				// connected to the same address as specified by the server, port
				// combination.
			Int32 port = 10000;
			TcpClient client = new TcpClient (server, port);
	
				// Translate the passed message into ASCII and store it as a Byte array.
			data = System.Text.Encoding.ASCII.GetBytes (message);         
				
				// Get a client stream for reading and writing.
			  Stream stream = client.GetStream();
				
				//NetworkStream stream = client.GetStream ();

				// Send the message to the connected TcpServer. 
			stream.Write (data, 0, data.Length);
			//Console.WriteLine("Sent: {0}", message);         
				
			// Receive the TcpServer.response.

			// Buffer to store the response bytes.
			data = new Byte[256];

			// String to store the response ASCII representation.
				//String responseData = String.Empty;
				
			// Read the first batch of the TcpServer response bytes.
			//Int32 bytes = stream.Read (data, 0, data.Length);
			//Debug.Log (System.Text.Encoding.ASCII.GetString (data));

			return stream;
				//responseData = System.Text.Encoding.ASCII.GetString (data, 0, bytes);
				//Debug.Log(responseData.ToString());
		} catch (ArgumentNullException e) {
			//Console.WriteLine("ArgumentNullException: {0}", e);
			Debug.Log (e);
			Debug.Log ("here1");
			Application.Quit();
			return null;
		} catch (SocketException e) {
			//Console.WriteLine("SocketException: {0}", e);
			Debug.Log (e);
			//Debug.Log ("here2");
			//Application.Quit();
			return null;
		}

		//Console.WriteLine("\n Press Enter to continue...");
		//Console.Read();
	}

}

