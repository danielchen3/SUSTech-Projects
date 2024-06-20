import java.util.Objects;

public class Passenger {

    private String name;

    private String idNumber;

    private String phoneNumber;

    private String gender;

    private String district;

    public String getName() {
        return name;
    }

    public void setName(String name) {
        this.name = name;
    }

    public String getIdNumber() {
        return idNumber;
    }

    public void setIdNumber(String idNumber) {
        this.idNumber = idNumber;
    }

    public String getPhoneNumber() {
        return phoneNumber;
    }

    public void setPhoneNumber(String phoneNumber) {
        this.phoneNumber = phoneNumber;
    }

    public String getGender() {
        return gender;
    }

    public void setGender(String gender) {
        this.gender = gender;
    }

    public String getDistrict() {
        return district;
    }

    public void setDistrict(String district) {
        this.district = district;
    }

    public Passenger(String name, String idNumber, String phoneNumber, String gender, String district) {
        this.name = name;
        this.idNumber = idNumber;
        this.phoneNumber = phoneNumber;
        this.gender = gender;
        this.district = district;
    }




    @Override
    public String toString() {
        return "Passenger{" +
                "name='" + name + '\'' +
                ", idNumber='" + idNumber + '\'' +
                ", phoneNumber='" + phoneNumber + '\'' +
                ", gender='" + gender + '\'' +
                ", district='" + district + '\'' +
                '}';
    }
}
