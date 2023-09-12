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
        byte[] buffer = new byte[client.ReceiveBufferSize];
        int bytesRead = nwStream.Read(buffer, 0, client.ReceiveBufferSize);

        string dataReceived = Encoding.UTF8.GetString(buffer, 0, bytesRead);
        
        if (!string.IsNullOrEmpty(dataReceived))
        {
            position = ParseData(dataReceived);
            nwStream.Write(buffer, 0, bytesRead);
        }
    }

    public static Vector3 ParseData(string dataString)
    {
        Debug.Log(dataString);
        if (dataString.StartsWith("(") && dataString.EndsWith(")"))
        {
            dataString = dataString.Substring(1, dataString.Length - 2);
        }

        string[] stringArray = dataString.Split(',');

        Vector3 result = new Vector3(
            float.Parse(stringArray[0]),
            float.Parse(stringArray[1]),
            float.Parse(stringArray[2]));

        return result;
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
