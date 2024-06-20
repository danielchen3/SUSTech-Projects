public class Station {
    private String stationName;
    private String district;
    private String intro;
    private String chineseName;

    // 构造方法
    public Station(String stationName, String district, String intro, String chineseName) {
        this.stationName = stationName;
        this.district = district;
        this.intro = intro;
        this.chineseName = chineseName;
    }

    // Getter 和 Setter 方法
    public String getStationName() {
        return stationName;
    }

    public void setStationName(String stationName) {
        this.stationName = stationName;
    }

    public String getDistrict() {
        return district;
    }

    public void setDistrict(String district) {
        this.district = district;
    }

    public String getIntro() {
        return intro;
    }

    public void setIntro(String intro) {
        this.intro = intro;
    }

    public String getChineseName() {
        return chineseName;
    }

    public void setChineseName(String chineseName) {
        this.chineseName = chineseName;
    }
}
