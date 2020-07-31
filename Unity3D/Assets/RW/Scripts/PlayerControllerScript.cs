using UnityEngine;
using System;
using System.Collections;
using System.Net;
using System.Net.Sockets;
using System.Text;
using System.Threading;
using System.Runtime.InteropServices.ComTypes;

public class PlayerControllerScript: MonoBehaviour 
{
	// 1. Declare Variables
	Thread receiveThread;
	UdpClient client;
	int port;

	public GameObject Player;
	AudioSource jumpSound;
	bool jump;
    bool rotateLeft;
    bool rotateRight;

    // 2. Initialize variables
    private void Start()
    {
        port = 5065;
        jump = false;
        jumpSound = gameObject.GetComponent<AudioSource>();
        InitUDP();
        rotateLeft = false;
        rotateRight = false;
    }
    // 3. InitUDP
    private void InitUDP()
    {
        print("UDP Initialised");
        receiveThread = new Thread(new ThreadStart(ReceiveData));
        receiveThread.IsBackground = true;
        receiveThread.Start();
    }
   

    // 4. Receive Data
    private void ReceiveData()
    {
        client = new UdpClient(port);
        while(true)
        {
            try
            {
                IPEndPoint anyIP = new IPEndPoint(IPAddress.Parse("0.0.0.0"), port);
                byte[] data = client.Receive(ref anyIP);
                string text = Encoding.UTF8.GetString(data);
                if (text == "Left!")
                {
                    rotateLeft = true;
                }
                else if (text == "Right!")
                {
                    rotateRight = true;
                }
                print(">> " + text);
                jump = true;
            }
            catch (Exception e)
            {
                print(e.ToString());
            }
        }
    }

    private void Rotate()
    {
        var temp = Player.transform.localEulerAngles;
        temp.y = -90;
        Player.transform.localEulerAngles = temp;
        Debug.Log(Player.transform.localEulerAngles);

    }

    // 5. Make the Player Jump
    public void Jump()
    {
        Player.GetComponent<Animator>().SetTrigger("Jump");
        jumpSound.PlayDelayed(44100);
    }

    // 6. Check for variable value, and make the Player Jump!
    private void Update()
    {
        if (jump == true)
        {
            Jump();
            jump = false;
            print("jumped");
        }
        if (rotateLeft == true)
        {
            Rotate();
            rotateLeft = false;
        }
        if (rotateRight == true)
        {
            RotateRight();
            rotateRight = false;
        }
    }

    private void RotateRight()
    {
        var temp = Player.transform.localEulerAngles;
        temp.y = 90;
        Player.transform.localEulerAngles = temp;
        Debug.Log(Player.transform.localEulerAngles);
    }
}
