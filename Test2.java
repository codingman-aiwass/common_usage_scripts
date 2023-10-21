package android;

public class Test2 {
    public static void main(String[] args) {
        for(String apkList:ReadApks.getApkList()){
            System.out.println(apkList);
            System.out.println(GetApkPackageName.get(apkList));
            System.out.println(GetApkPackageName.getAppName(apkList));
            System.out.println("=========");
        }
//        System.out.println(GetApkPackageName.getAppName("C:/Users/HP/myfiles/privacy_compliance/apks/com.youku.phone_11.0.17_587.apk"));
    }
}