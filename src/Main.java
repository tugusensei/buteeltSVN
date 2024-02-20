import java.util.Scanner;

public class Main {
    public static void main(String[] args) {
        Scanner scanner = new Scanner(System.in);
        Queue<Integer> integerQueue = new Queue<>();

        while (true) {
            System.out.println("\nХийх үйлдэлээ сонгоно уу:");
            System.out.println("1. Нэмэх");
            System.out.println("2. Хасах");
            System.out.println("3. Front");
            System.out.println("4. Хэмжээ");
            System.out.println("5. Харуулах");
            System.out.println("6. Цэвэрлэх");
            System.out.println("7. Гарах");

            int choice = scanner.nextInt();

            switch (choice) {
                case 1:
                    System.out.println("Нэмэх элементээ оруулна уу:");
                    int element = scanner.nextInt();
                    integerQueue.enqueue(element);
                    System.out.println(element + " амжилттай нэмэгдлээ.");
                    break;
                case 2:
                    Integer dequeued = integerQueue.dequeue();
                    if (dequeued != null)
                        System.out.println("Хасагдсан элемент: " + dequeued);
                    break;
                case 3:
                    Integer frontElement = integerQueue.front();
                    if (frontElement != null)
                        System.out.println("Эхний элемент: " + frontElement);
                    break;
                case 4:
                    System.out.println("Дараалалын хэмжээ: " + integerQueue.size());
                    break;
                case 5:
                    integerQueue.display();
                    break;
                case 6:
                    integerQueue.clear();
                    System.out.println("Дараалал цэвэрлэгдлээ.");
                    break;
                case 7:
                    System.out.println("Гарч байна...");
                    System.exit(0);
                    break;
                default:
                    System.out.println("Invalid choice.");
            }
        }
    }
}
