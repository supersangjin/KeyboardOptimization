import java.io.File;
import java.io.FileNotFoundException;
import java.io.FileReader;
import java.io.FileWriter;
import java.io.IOException;
import java.io.StringWriter;
import java.util.ArrayList;
import java.util.Scanner;
import java.util.Set;

import org.w3c.dom.Text;

public class ReaderWriter {
	/**
	 * Reads lines of text to send to the client.
	 * @param fileName
	 * @return
	 * @throws FileNotFoundException
	 */
	public static String[] readstringsFromFile(String fileName) throws FileNotFoundException {
		Scanner scan = new Scanner(new File(fileName));
		ArrayList<String> linesList = new ArrayList<String>();
		
		while(scan.hasNext()) {
			linesList.add(scan.nextLine());
		}
		
		String[] linesArr = new String[linesList.size()];
		linesArr = linesList.toArray(linesArr);
		
		return linesArr;
	}

	/**
	 * Appends the received message and coordinate from the server to the OUTPUT_FILE.
	 * @param message
	 * @throws IOException
	 */
	public static void writeToFile(String message) throws IOException {
		String[] texts = message.split("_");
		
		if(texts.length > 0) {
			File f = new File(Constants.OUTPUT_FILE);
			FileWriter fw;
			if(f.exists() && !f.isDirectory()) { 
				fw = new FileWriter(Constants.OUTPUT_FILE, true);
			}
			else {
				fw = new FileWriter(Constants.OUTPUT_FILE);
			}
			// The first element in the texts array is the text message. The rest are coordinates.
			
			StringWriter sw = new StringWriter();
			
			for(int i = 0; i < texts.length; i++) {
				sw.write(texts[i]);
				sw.write(System.lineSeparator());
			}
			
			fw.write(sw.toString());
			fw.close();
		}
	}
}
