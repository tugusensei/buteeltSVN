public class Main {
    public static void main(String[] args) {
        // 
        Queue<Integer> integerQueue = new Queue<>();

        // 
        integerQueue.enqueue(1);
        integerQueue.enqueue(2);
        integerQueue.enqueue(3);

        // 
        System.out.print("Initial ");
        integerQueue.display(); 

        
        System.out.println("Dequeue: " + integerQueue.dequeue()); 
     
        System.out.print("Updated ");
        integerQueue.display(); 

      
        Integer frontElement = integerQueue.front();
        if (frontElement != null) {
            System.out.println("Front: " + frontElement); 

        // 
        System.out.println("Queue size: " + integerQueue.size()); 
    }
        integerQueue.clear();
        System.out.print("Cleared ");
        integerQueue.display();
        System.out.println("Queue has been cleared.");
}
}
