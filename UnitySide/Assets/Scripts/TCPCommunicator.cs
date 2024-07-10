using UnityEngine;
using System;
using System.Net;
using System.Net.Sockets;
using System.IO;
using System.Text;

public class TCPCommunicator : MonoBehaviour
{
    Promise promise;
    Socket socket;
    float ellapsed = 0;
    byte[] data = new byte[1024];
    bool bHandshakeSuccessful = false;

    void Start()
    {
        string path = "Assets/promise.json";
        StreamReader reader = new StreamReader(path);
        string contents = reader.ReadToEnd();
        reader.Close();

        promise = JsonUtility.FromJson<Promise>(contents);
        socket = new Socket(AddressFamily.InterNetwork, SocketType.Stream, ProtocolType.Tcp);
        IPAddress ip = IPAddress.Parse(promise.ip);
        IPEndPoint ep = new IPEndPoint(ip, promise.port);
        try
        {
            Debug.Log("Connecting to server...");
            socket.Connect(ep);
        }
        catch (SocketException e)
        {
            Debug.LogError("Connection Failed!");
            Debug.Log(e.ToString());
            return;
        }
        Debug.Log("First handshake test");
        Send(promise.begin);
        string resp = Receive();
        if (resp.Equals(promise.begin))
        {
            Debug.Log("Connection Established");
            bHandshakeSuccessful = true;
        }
        else
        {
            Debug.Log("First hankshake failed");
            socket.Close();
        }
    }

    private void Update()
    {
        if (!bHandshakeSuccessful)
            return;
        ellapsed += Time.deltaTime;
        string s = "Hello";
        if (ellapsed > 1)
        {
            try
            {
                ellapsed -= 1;
                socket.Send(Encoding.UTF8.GetBytes(s));
                socket.Receive(data);
                Debug.Log(Encoding.UTF8.GetString(data));
            }
            catch (SocketException e)
            {
                Debug.LogError("Connection has been cancelled from remote");
                Debug.Log(e.ToString());
                bHandshakeSuccessful = false;
                Application.Quit();
            }
        }
    }

    private void OnDestroy()
    {
        if(bHandshakeSuccessful)
        {
            socket.Send(Encoding.UTF8.GetBytes(promise.end));
            socket.Close();
        }
    }

    void Send(string data)
    {
        socket.Send(Encoding.UTF8.GetBytes(data));
    }

    string Receive()
    {
        socket.Receive(data);
        string resp = Encoding.UTF8.GetString(data);
        resp = resp.Trim('\0');
        Array.Clear(data, 0, resp.Length);
        return resp;
    }
}
