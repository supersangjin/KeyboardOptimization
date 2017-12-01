import javax.swing.*;
import java.io.*;
import java.net.Inet6Address;
import java.net.InetAddress;
import java.net.ServerSocket;
import java.net.Socket;
import java.net.UnknownHostException;
import java.util.Enumeration;
import java.net.NetworkInterface;
 
/**
 * The class extends the Thread class so we can receive and send messages at the same time
 *
 * @author Catalin Prata
 *         Date: 2/12/13
 */
public class TcpServer extends Thread {
 
    public static final int SERVERPORT = 4444;
    // while this is true the server will run
    private boolean running = false;
    // used to send messages
    private PrintWriter bufferSender;
    // callback used to notify new messages received
    private OnMessageReceived messageListener;
    private ServerSocket serverSocket;
    private Socket client;
 
    /**
     * Constructor of the class
     *
     * @param messageListener listens for the messages
     */
    public TcpServer(OnMessageReceived messageListener) {
        this.messageListener = messageListener;
    }
 
    public static void main(String[] args) {
 
        //opens the window where the messages will be received and sent
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
 
        System.out.println("S: Done.");
        serverSocket = null;
        client = null;
 
    }
 
    /**
     * Method to send the messages from server to client
     *
     * @param message the message sent by the server
     */
    public void sendTextFile(String[] messages) {
        if (bufferSender != null && !bufferSender.checkError()) {
        	for(int i = 0; i < messages.length; i++) {
        		bufferSender.println(messages[i]);
        	}
            bufferSender.flush();
        }
    }
    
    /**
     * Method to send the messages from server to client
     *
     * @param message the message sent by the server
     */
    public void sendMessage(String message) {
        if (bufferSender != null && !bufferSender.checkError()) {
        	bufferSender.println(message);
            bufferSender.flush();
        }
    }
 
    public boolean hasCommand(String message) {
        if (message != null) {
            if (message.contains(Constants.CLOSED_CONNECTION)) {
                messageListener.messageReceived("Disconnected");
                // close the server connection if we have this command and rebuild a new one
                close();
                runServer();
                return true;
            } else if (message.contains(Constants.LOGIN_NAME)) {
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
        	String ip = getLocalHostLANAddress().toString();
        	
        	 messageListener.messageReceived("IP: " + ip);
        	
            System.out.println("S: Connecting...");
 
            //create a server socket. A server socket waits for requests to come in over the network.
            serverSocket = new ServerSocket(SERVERPORT);
 
            //create client socket... the method accept() listens for a connection to be made to this socket and accepts it.
            client = serverSocket.accept();
 
            System.out.println("S: Receiving...");
 
            try {
 
                //sends the message to the client
                bufferSender = new PrintWriter(new BufferedWriter(new OutputStreamWriter(client.getOutputStream())), true);
 
                //read the message received from client
                BufferedReader in = new BufferedReader(new InputStreamReader(client.getInputStream()));
 
                //in this while we wait to receive messages from client (it's an infinite loop)
                //this while it's like a listener for messages
                while (running) {
 
                    String message = null;
                    try {
                        message = in.readLine();
                    } catch (IOException e) {
                        System.out.println("Error reading message: " + e.getMessage());
                    }
 
                    if (hasCommand(message)) {
                        continue;
                    }
 
                    if (message != null && messageListener != null) {
                        //call the method messageReceived from ServerBoard class
                        messageListener.messageReceived(message);
                    }
                }
 
            } catch (Exception e) {
                System.out.println("S: Error");
                e.printStackTrace();
            }
 
        } catch (Exception e) {
            System.out.println("S: Error");
            e.printStackTrace();
        }
    }
 
    @Override
    public void run() {
        super.run();
 
        runServer();
 
    }
 
    //Declare the interface. The method messageReceived(String message) will must be implemented in the ServerBoard
    //class at on startServer button click
    public interface OnMessageReceived {
        public void messageReceived(String message);
    }
 
    private static InetAddress getLocalHostLANAddress() throws UnknownHostException
    {
        try
        {
            InetAddress candidateAddress = null;
            // Iterate all NICs (network interface cards)...
            for (Enumeration<NetworkInterface> ifaces = NetworkInterface.getNetworkInterfaces(); ifaces.hasMoreElements();)
            {
                NetworkInterface iface = (NetworkInterface) ifaces.nextElement();
                // Iterate all IP addresses assigned to each card...
                for (Enumeration<InetAddress> inetAddrs = iface.getInetAddresses(); inetAddrs.hasMoreElements();)
                {
                    InetAddress inetAddr = (InetAddress) inetAddrs.nextElement();
                    if (!inetAddr.isLoopbackAddress())
                    {
                    	if (inetAddr instanceof Inet6Address) continue;
                        if (inetAddr.isSiteLocalAddress())
                        {
                            // Found non-loopback site-local address. Return it immediately...
                            return inetAddr;
                        }
                        else if (candidateAddress == null)
                        {
                            // Found non-loopback address, but not necessarily site-local.
                            // Store it as a candidate to be returned if site-local address is not subsequently found...
                            candidateAddress = inetAddr;
                            // Note that we don't repeatedly assign non-loopback non-site-local addresses as candidates,
                            // only the first. For subsequent iterations, candidate will be non-null.
                        }
                    }
                }
            }
            if (candidateAddress != null)
            {
                // We did not find a site-local address, but we found some other non-loopback address.
                // Server might have a non-site-local address assigned to its NIC (or it might be running
                // IPv6 which deprecates the "site-local" concept).
                // Return this non-loopback candidate address...
                return candidateAddress;
            }
            // At this point, we did not find a non-loopback address.
            // Fall back to returning whatever InetAddress.getLocalHost() returns...
            InetAddress jdkSuppliedAddress = InetAddress.getLocalHost();
            if (jdkSuppliedAddress == null) {
                throw new UnknownHostException("The JDK InetAddress.getLocalHost() method unexpectedly returned null.");
            }
            return jdkSuppliedAddress;
        }
        catch (Exception e)
        {
            UnknownHostException unknownHostException = new UnknownHostException("Failed to determine LAN address: " + e);
            unknownHostException.initCause(e);
            throw unknownHostException;
        }
    }

    
}

