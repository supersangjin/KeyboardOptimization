import javax.swing.*;
import java.awt.event.ActionEvent;
import java.awt.event.ActionListener;
import java.io.FileNotFoundException;
import java.io.IOException;
 
/**
 * Description
 *
 * @author Catalin Prata
 *         Date: 2/12/13
 */
public class MainScreen extends JFrame {
 
	private JScrollPane scrollPane;
    private JTextArea messagesArea;
    private JButton sendButton;
    private JTextField message;
    private JButton startServer;
    private JButton stopServer;
    private JButton sendTextFile;
    private TcpServer mServer;
 
    public MainScreen() {
 
        super("MainScreen");
 
        JPanel panelFields = new JPanel();
        panelFields.setLayout(new BoxLayout(panelFields, BoxLayout.X_AXIS));
 
        JPanel panelFields2 = new JPanel();
        panelFields2.setLayout(new BoxLayout(panelFields2, BoxLayout.X_AXIS));
 
        //here we will have the text messages screen
        messagesArea = new JTextArea();
        messagesArea.setColumns(30);
        messagesArea.setRows(30);
        messagesArea.setEditable(false);
        
        scrollPane = new JScrollPane(messagesArea);
 
        sendButton = new JButton("Send");
        sendButton.addActionListener(new ActionListener() {
            @Override
            public void actionPerformed(ActionEvent e) {
                // get the message from the text view
                String messageText = message.getText();
                // add message to the message area
                messagesArea.append("\n " + messageText);
                if (mServer != null) {
                    // send the message to the client
                    mServer.sendMessage(messageText);
                }
                // clear text
                message.setText("");
            }
        });
 
        startServer = new JButton("Start");
        startServer.addActionListener(new ActionListener() {
            @Override
            public void actionPerformed(ActionEvent e) {
 
                //creates the object OnMessageReceived asked by the TCPServer constructor
                mServer = new TcpServer(new TcpServer.OnMessageReceived() {
                    @Override
                    //this method declared in the interface from TCPServer class is implemented here
                    //this method is actually a callback method, because it will run every time when it will be called from
                    //TCPServer class (at while)
                    public void messageReceived(String message) {
                        try {
                        	messagesArea.append("\n " + message);
                        	if(!(message.equals("Device connected!") || message.contains("IP: "))) {
                        		ReaderWriter.writeToFile(message);
                        	}
						} catch (IOException e) {
							messagesArea.append("\n Cannot write to file");
						}
                    }
                });
                mServer.start();
 
                // disable the start button and enable the stop one
                startServer.setEnabled(false);
                stopServer.setEnabled(true);
 
            }
        });
 
        stopServer = new JButton("Stop");
        stopServer.addActionListener(new ActionListener() {
            @Override
            public void actionPerformed(ActionEvent e) {
 
                if (mServer != null) {
                    mServer.close();
                }
 
                // disable the stop button and enable the start one
                startServer.setEnabled(true);
                stopServer.setEnabled(false);
            }
        });
        
        sendTextFile = new JButton("Send text file strings");
        sendTextFile.addActionListener(new ActionListener() {
            @Override
            public void actionPerformed(ActionEvent e) {
                try {
	                String[] lines = ReaderWriter.readstringsFromFile("textToSend.txt");
	                
	                messagesArea.append("\n Sending text file containing:");
	                for(int i = 0; i < lines.length; i++) {
	                	messagesArea.append("\n " + i + ": " + lines[i]);
	                }
	                if (mServer != null) {
	                    // send the message to the client
	                    mServer.sendTextFile(lines);
	                }
                }
                catch(FileNotFoundException exception) {
                	messagesArea.append("\n Cannot read the file.");
                }
            }
        });
 
        //the box where the user enters the text (EditText is called in Android)
        message = new JTextField();
        message.setSize(200, 20);
 
        //add the buttons and the text fields to the panel
        panelFields.add(scrollPane);
        panelFields.add(startServer);
        panelFields.add(stopServer);
        panelFields.add(sendTextFile);
 
        panelFields2.add(message);
        panelFields2.add(sendButton);
 
        getContentPane().add(panelFields);
        getContentPane().add(panelFields2);
 
        getContentPane().setLayout(new BoxLayout(getContentPane(), BoxLayout.Y_AXIS));
 
        setSize(300, 170);
        setVisible(true);
    }
 
}