//read emotions
//Written by Matt Shenton
//12/5/17
//purpose: read in strings from "emotions" text file

import java.io.*;

public class EmotionReader{
	public EmotionReader(){}

	public void readEmotions(){

		String line = null;

		try {

		//FileReader input = new FileReader("emotions");

			BufferedReader b = new BufferedReader(new FileReader("emotions"));

			line = b.readLine();

			while(line != null){

				System.out.println(line);

				//Do something, TBD, with line
				
				line = b.readLine();
			}
			b.close();

		}

		catch(IOException e){
			System.out.println("Couldn't read file!");
		}
	}
}