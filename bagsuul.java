import java.util.ArrayList;
import java.util.HashMap;
import java.util.List;
import java.util.Map;

class Employee {
    private String name;
    private int id;
    private String department;

    public Employee(String name, int id, String department) {
        this.name = name;
        this.id = id;
        this.department = department;
    }

    public String getName() {
        return name;
    }

    public int getId() {
        return id;
    }

    public String getDepartment() {
        return department;
    }

    @Override
    public String toString() {
        return "Employee{" +
                "name='" + name + '\'' +
                ", id=" + id +
                ", department='" + department + '\'' +
                '}';
    }
}

public class EmployeeTransfer {

    public static void main(String[] args) {
        // Sample employee information
        List<Employee> employees = new ArrayList<>();
        employees.add(new Employee("John Doe", 101, "HR"));
        employees.add(new Employee("Jane Smith", 102, "Finance"));
        employees.add(new Employee("Michael Johnson", 103, "IT"));

        // Separate employee information
        Map<String, List<Employee>> departmentMap = new HashMap<>();
        for (Employee employee : employees) {
            String department = employee.getDepartment();
            if (!departmentMap.containsKey(department)) {
                departmentMap.put(department, new ArrayList<>());
            }
            departmentMap.get(department).add(employee);
        }

        // Simulate transferring information to backup server
        System.out.println("Transferring employee information to backup server...");
        for (Map.Entry<String, List<Employee>> entry : departmentMap.entrySet()) {
            String department = entry.getKey();
            List<Employee> departmentEmployees = entry.getValue();
            System.out.println("Department: " + department);
            System.out.println("Employees: " + departmentEmployees);
            // Logic to transfer the information to the backup server goes here
        }
        System.out.println("Transfer completed.");
    }
}
