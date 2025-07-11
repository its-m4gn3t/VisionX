using SocketIO;
using UnityEngine;

public class SocketManager : MonoBehaviour
{
    private SocketIOComponent socket;

    void Start()
    {
        GameObject go = GameObject.Find("SocketIO");
        socket = go.GetComponent<SocketIOComponent>();

        socket.On("open", OnConnected);
        socket.On("error", OnError);
        socket.On("close", OnDisconnected);

        // Listen to custom events from server
        socket.On("gameEvent", OnGameEvent);

        socket.Connect();
    }

    void OnConnected(SocketIOEvent e)
    {
        Debug.Log("Connected to server");
    }

    void OnError(SocketIOEvent e)
    {
        Debug.Log("Socket error: " + e.data);
    }

    void OnDisconnected(SocketIOEvent e)
    {
        Debug.Log("Disconnected from server");
    }

    void OnGameEvent(SocketIOEvent e)
    {
        Debug.Log("Received game event: " + e.data);
        // Parse and handle game data here
    }

    // Example to emit event to server
    public void SendPlayerAction(string action)
    {
        socket.Emit("playerAction", new JSONObject($"{{\"action\":\"{action}\"}}"));
    }
}
