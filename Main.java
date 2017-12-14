public class Main {
		
	public static void main (String[] args){
		java.awt.EventQueue.invokeLater(new Runnable(){
			public void run(){
				new Main();
			}
		});
	}

	public Main(){

		EmotionReader e = new EmotionReader();

		for (int i = 0; i < 4; i++) {
			//if (e.readNextEmotion)
			//System.out.println(e.readNextEmotion(i));
			String emotion = e.readNextEmotion(i);
			if (emotion == null){
				System.out.println("Nothing new");
			}
			else System.out.println(emotion);
		}

		
	}
}