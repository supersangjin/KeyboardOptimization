import javax.swing.*;
import java.io.*;
import java.net.InetAddress;
import java.net.ServerSocket;
import java.net.Socket;
 
public class TcpServer extends Thread {
 
    public static final int SERVERPORT = 4444;
    private boolean running = false;
    private PrintWriter bufferSender;
    private OnMessageReceived messageListener;
    private ServerSocket serverSocket;
    private Socket client;
 
    /**
     * Constructor
     *
     * @param messageListener listens for the messages
     */
    public TcpServer(OnMessageReceived messageListener) {
        this.messageListener = messageListener;
    }
 
    public static void main(String[] args) {
        MainScreen frame = new MainScreen();
        frame.setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE);
        frame.pack();
        frame.setVisible(true);
    }
 
    /**
     * Close the server
     */
    public void close() {
 
        running = false;
 
        if (bufferSender != null) {
            bufferSender.flush();
            bufferSender.close();
            bufferSender = null;
        }
 
        try {
            client.close();
            serverSocket.close();
        } catch (Exception e) {
            e.printStackTrace();
        }
 
        System.out.println("Done");
        serverSocket = null;
        client = null;
 
    }
 
    /**
     * Sends the messages to the client
     *
     * @param message the message sent by the server
     */
    public void sendTextFile(String[] messages) {
        if (bufferSender != null && !bufferSender.checkError()) {
        	for(int i = 0; i < messages.length; i++) {
        		bufferSender.println(messages[i]);
        		bufferSender.flush();
        	}
        }
    }
    
    /**
     * Sends the message to the client
     *
     * @param message the message sent by the server
     */
    public void sendMessage(String message) {
        if (bufferSender != null && !bufferSender.checkError()) {
        	bufferSender.println(message);
            bufferSender.flush();
        }
    }
 
    /**
     * When an initial greeting message is received from the client, this method returns true.
     * This is to indicate when a device has just connected to the server.
     * @param message
     * @return
     */
    public boolean deviceConnected(String message) {
        if (message != null) {
            if (message.contains(Constants.LOGIN_NAME)) {
                messageListener.messageReceived("Device connected!");
                
                return true;
            }
        }
 
        return false;
    }
 
    /**
     * Builds a new server connection
     */
    private void runServer() {
        running = true;
 
        try {
        	String ip = InetAddress.getLocalHost().toString();
        	
        	System.out.println("IP: " + ip);
        	
            System.out.println("Pending connection");
 
            //create a server socket. A server socket waits for requests to come in over the network.
            serverSocket = new ServerSocket(SERVERPORT);
 
            //create client socket... the method accept() listens for a connection to be made to this socket and accepts it.
            client = serverSocket.accept();
 
            System.out.println("Receiving Data");
 
            try {
 
                // Used to send messages to the client
                bufferSender = new PrintWriter(new BufferedWriter(new OutputStreamWriter(client.getOutputStream())), true);
 
                // Used to read messages from the client
                BufferedReader in = new BufferedReader(new InputStreamReader(client.getInputStream()));
 
                // This loop listens to new messages
                while (running) {
 
                    String message = null;
                    try {
                        message = in.readLine();
                    } catch (IOException e) {
                        System.out.println("Error reading message: " + e.getMessage());
                    }
 
                    // If a device just connected, nothing further is done.
                    if (deviceConnected(message)) {
                        continue;
                    }
 
                    if (message != null && messageListener != null) {
                        messageListener.messageReceived(message);
                    }
                }
 
            } catch (Exception e) {
                System.out.println("Error");
                e.printStackTrace();
            }
 
        } catch (Exception e) {
            System.out.println("Error");
            e.printStackTrace();
        }
    }
 
    @Override
    public void run() {
        super.run();
 
        runServer();
 
    }
    
    public interface OnMessageReceived {
        public void messageReceived(String message);
    }
 
}