using System.Net;
using System.Net.Sockets;
using System.Text;
using UnityEngine;
using System.Threading;

public class MyListener : MonoBehaviour
{
    Thread listenThread;
    public int connectionPort = 25001;
    TcpListener server;
    bool running;

    void Start()
    {
        // Start listening for client connections on a separate thread
        ThreadStart ts = new ThreadStart(ListenForClients);
        listenThread = new Thread(ts);
        listenThread.Start();
    }

    void ListenForClients()
    {
        server = new TcpListener(IPAddress.Any, connectionPort);
        server.Start();
        running = true;

        while (running)
        {
            TcpClient newClient = server.AcceptTcpClient();

            // Start a new thread to handle this client's data
            Thread clientThread = new Thread(new ParameterizedThreadStart(HandleClient));
            clientThread.Start(newClient);
        }
    }

    void HandleClient(object obj)
    {
        TcpClient client = (TcpClient)obj;

        bool clientConnected = true;

        while (clientConnected && running)
        {
            try
            {
                Connection(client);
            }
            catch (SocketException)
            {
                // Handle client disconnection or other socket related errors here.
                clientConnected = false;
            }
        }
        
        client.Close();
    }

    void Connection(TcpClient client)
    {
        NetworkStream nwStream = client.GetStream();
        byte[] buffer = new byte[12]; // 3 floats * 4 bytes each
        int bytesRead = nwStream.Read(buffer, 0, buffer.Length);

        if (bytesRead == 12)
        {
            position = ParseData(buffer);
            nwStream.Write(buffer, 0, bytesRead);
        }
    }

    public Vector3 ParseData(byte[] data)
    {
        float x = System.BitConverter.ToSingle(data, 0);
        float y = System.BitConverter.ToSingle(data, 4);
        float z = System.BitConverter.ToSingle(data, 8);

        return new Vector3(x, y, z);
    }

    Vector3 position = Vector3.zero;

    void Update()
    {
        // Get the current position
        Vector3 currentPosition = transform.position;

        // Adjust the current position by the parsed values
        currentPosition += position;

        // Set the new position
        transform.position = currentPosition;
    }

    // Cleanup and close the server when the application is closed or this object is destroyed.
    void OnDestroy()
    {
        running = false;
        server?.Stop();
        listenThread?.Join();
    }
}
