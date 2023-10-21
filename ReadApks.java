package android;

import java.io.File;
import java.io.FileFilter;
import java.io.FileNotFoundException;
import java.io.FileReader;
import java.io.IOException;
import java.nio.file.Paths;
import java.util.ArrayList;
import java.util.Properties;

public class ReadApks {
    public static ArrayList<String> getApkList(){
        ArrayList<String> apksToAnalysis = new ArrayList<>();
        ArrayList<String> apkFoldersToAnalysis = new ArrayList<>();
        // 判断输入的apk参数是否包含多个apk的绝对路径,或者包含多个文件夹的绝对路径
        Properties properties = new Properties();
        try {
            properties.load(new FileReader("RunningConfig.properties"));
        } catch (FileNotFoundException e) {
            e.printStackTrace();
        } catch (IOException e) {
            e.printStackTrace();
        }
        String apkPath = Paths.get(properties.getProperty("apk", "")).toString();
//        String apkPath = properties.getProperty("apk", "");
        String[] apks = apkPath.split(";");
        if (apks.length == 1) {
            // 说明只输入了一个绝对路径,判断这个绝对路径是apk的还是文件夹的
            if (apks[0].endsWith(".apk")) {
                // 表示输入了一个apk的绝对路径
                apksToAnalysis.add(apks[0]);
            } else {
                // 表示输入了一个文件夹的绝对路径
                apkFoldersToAnalysis.add(apks[0]);
            }
        } else if (apks.length > 1) {
            // 说明输入了多个apk或者文件夹的绝对路径
            for (String apk : apks) {
                if (apk.endsWith(".apk")) {
                    apksToAnalysis.add(apk);
                } else {
                    apkFoldersToAnalysis.add(apk);
                }
            }
        } else {
            return null;
        }
        
        ArrayList<String> totalApks = new ArrayList<>();
        totalApks.addAll(apksToAnalysis);
        for (String apksFolder : apkFoldersToAnalysis) {
            File[] apkList = new File(apksFolder).listFiles(new FileFilter() {
                public boolean accept(File file) {
                    return file.isFile() && file.getName().endsWith(".apk");
                }
            });
            if (apkList == null) {
                continue;
            }
            for (File apkFile : apkList) {
                totalApks.add(apkFile.getAbsolutePath());
            }
        }
        return totalApks;
    }
}
