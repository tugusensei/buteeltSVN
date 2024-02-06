import java.util.LinkedList;


public class Queue<T> {
    private LinkedList<T> items;

    public Queue() {
        this.items = new LinkedList<>();
    }

    public void enqueue(T item) {
        // 
        items.addLast(item);
    }

    public T dequeue() {
        //
        if (!isEmpty()) {
            return items.removeFirst();
        } else {
            System.out.println("Queue is empty.");
            return null;
        }
    }

    public boolean isEmpty() {
        // 
        return items.isEmpty();
    }

    public int size() {
        // 
        return items.size();
    }

    public T front() {
        //
        if (!isEmpty()) {
            return items.getFirst();
        } else {
            System.out.println("Queue is empty.");
            return null;
        }
    }

    public void display() {
        //
        System.out.print("Queue: ");
        for (T item : items) {
            System.out.print(item + " ");
        }
        System.out.println();
    }
    public void clear() {
        items.clear();
        System.out.println("Queue has been cleared.");
    }
}
//14:44

