//read emotions
//Written by Matt Shenton
//12/5/17
//purpose: read in strings from "emotions" text file

import java.io.*;

public class EmotionReader{
	
	private static int current_lineNum;

	public EmotionReader(){
		current_lineNum = -1;
	}

	public static String readNextEmotion(int lineNum){
		
		File file = new File("emotions");
		String lastLine = tail(file);
		
		String[] words = lastLine.split(" ");

		if (Integer.parseInt(words[0]) > current_lineNum){
			current_lineNum++;
			return words[1];
		}
		return null;

	}

	//https://stackoverflow.com/questions/686231/quickly-read-the-last-line-of-a-text-file

	public static String tail( File file ) {
    	RandomAccessFile fileHandler = null;
    	try {
        	fileHandler = new RandomAccessFile( file, "r" );
        	long fileLength = fileHandler.length() - 1;
        	StringBuilder sb = new StringBuilder();

        	for(long filePointer = fileLength; filePointer != -1; filePointer--){
            	fileHandler.seek( filePointer );
            	int readByte = fileHandler.readByte();

            	if( readByte == 0xA ) {
                	if( filePointer == fileLength ) {
                    	continue;
                	}
                	break;

            	} else if( readByte == 0xD ) {
                	if( filePointer == fileLength - 1 ) {
                    	continue;
                	}
                	break;
            	}

            	sb.append( ( char ) readByte );
        	}

        	String lastLine = sb.reverse().toString();
        	return lastLine;
    	} catch( java.io.FileNotFoundException e ) {
        	e.printStackTrace();
        	return null;
    	} catch( java.io.IOException e ) {
        	e.printStackTrace();
        	return null;
    	} finally {
        	if (fileHandler != null )
            	try {
                	fileHandler.close();
            	} catch (IOException e) {
                /* ignore */
            	}
    		}
		}
}

