/*
 * This file is part of the LIRE project: http://www.semanticmetadata.net/lire
 * LIRE is free software; you can redistribute it and/or modify
 * it under the terms of the GNU General Public License as published by
 * the Free Software Foundation; either version 2 of the License, or
 * (at your option) any later version.
 *
 * LIRE is distributed in the hope that it will be useful,
 * but WITHOUT ANY WARRANTY; without even the implied warranty of
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 * GNU General Public License for more details.
 *
 * You should have received a copy of the GNU General Public License
 * along with LIRE; if not, write to the Free Software
 * Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA  02111-1307  USA
 *
 * We kindly ask you to refer the any or one of the following publications in
 * any publication mentioning or employing Lire:
 *
 * Lux Mathias, Savvas A. Chatzichristofis. Lire: Lucene Image Retrieval �C
 * An Extensible Java CBIR Library. In proceedings of the 16th ACM International
 * Conference on Multimedia, pp. 1085-1088, Vancouver, Canada, 2008
 * URL: http://doi.acm.org/10.1145/1459359.1459577
 *
 * Lux Mathias. Content Based Image Retrieval with LIRE. In proceedings of the
 * 19th ACM International Conference on Multimedia, pp. 735-738, Scottsdale,
 * Arizona, USA, 2011
 * URL: http://dl.acm.org/citation.cfm?id=2072432
 *
 * Mathias Lux, Oge Marques. Visual Information Retrieval using Java and LIRE
 * Morgan & Claypool, 2013
 * URL: http://www.morganclaypool.com/doi/abs/10.2200/S00468ED1V01Y201301ICR025
 *
 * Copyright statement:
 * ====================
 * (c) 2002-2013 by Mathias Lux (mathias@juggle.at)
 *  http://www.semanticmetadata.net/lire, http://www.lire-project.net
 *
 * Updated: 20.04.13 09:05
 */

package net.semanticmetadata.lire;


import net.semanticmetadata.lire.imageanalysis.features.global.*;
import net.semanticmetadata.lire.utils.FileUtils;

import javax.imageio.ImageIO;
import java.awt.image.BufferedImage;
import java.io.*;
import java.util.*;

public class CEDDTest {
    public static void main(String[] args) throws IOException, IllegalAccessException, InstantiationException {
        int i =1;
        while (i <= 20){
            String path = "..\\..\\data\\reports\\" + String.valueOf(i) +
                    "\\app" + String.valueOf(i) + ".csv";
            String line = "";
            String SplitBy = ",";
            String[] Line;
            List<String[]> BikeDataList = new ArrayList<>();
            List<String> indexes = new ArrayList<>();
            List<String> urls = new ArrayList<>();

            try ( InputStreamReader isr = new InputStreamReader(new FileInputStream(path), "UTF-8");
                  BufferedReader br = new BufferedReader(isr)) {
                while ((line = br.readLine()) != null) {
                    Line = line.split(SplitBy);
                    indexes.add(Line[0]);
                    urls.add(Line[4]);
                }
            } catch (IOException e) {
                e.printStackTrace();
            }
            indexes.remove(0);
            urls.remove(0);
            List<String> EdgeHistograms = new ArrayList<>();
            List<String> ColorLayouts = new ArrayList<>();
            List<String> ScalableColors = new ArrayList<>();
            List<String> CEDDs = new ArrayList<>();
            for(int j = 0; j < indexes.size(); j++){
                EdgeHistogram eh1 = new EdgeHistogram();
                ColorLayout p1 = new ColorLayout();
                ScalableColor sch = new ScalableColor();
                CEDD cedd = new CEDD();
                String index = indexes.get(j);
                String[] url_types = urls.get(j).split("\\.");
                String url_type;

                if (Objects.equals(index, "378")){
                    url_type = urls.get(j).substring(urls.get(j).length()-4);
                }
                else {
                    url_type = urls.get(j).substring(urls.get(j).length()-3);
                }

                String imagePath = "..\\..\\data\\reports\\"  + String.valueOf(i) + "\\images\\"+index + "." + url_type;
                System.out.println(imagePath);
                BufferedImage image = ImageIO.read(new File(imagePath));

                try{
                    sch.extract(image);
                    ScalableColors.add(Arrays.toString(sch.getFeatureVector()));}
                catch (Exception e) {
                    System.out.println(imagePath + "ScalableColor error");
                }

                try{
                    eh1.extract(image);
                    EdgeHistograms.add(Arrays.toString(eh1.getFeatureVector()));}
                catch (Exception e) {
                    System.out.println(imagePath + "EdgeHistograms error");
                }
                try{
                    cedd.extract(image);
                    CEDDs.add(Arrays.toString(cedd.getFeatureVector()));
                }
                catch (Exception e) {
                    System.out.println(imagePath + "ColorLayouts error");
                }

                try{
                    p1.extract(image);
                    ColorLayouts.add(Arrays.toString(p1.getFeatureVector()));
                }
                catch (Exception e) {
                    System.out.println(imagePath + "ColorLayouts error");
                }

            }
                String Path1 = "..\\..\\output\\"  + String.valueOf(i) + "\\EdgeHistogram.txt";
                String Path2 = "..\\..\\output\\"  + String.valueOf(i) + "\\ColorLayout.txt";
                String Path3 = "..\\..\\output\\"  + String.valueOf(i) + "\\ScalableColor.txt";
                String Path4 = "..\\..\\output\\"  + String.valueOf(i) + "\\CEDD.txt";
                BufferedWriter bw;
                System.out.println(CEDDs);

            try {
                bw = new BufferedWriter(new FileWriter(Path4));
                for (int m = 0; m < CEDDs.size(); m++) {
                    bw.write(CEDDs.get(m));
                    bw.newLine();
                    bw.flush();
                }
                bw.close();
            } catch (IOException e) {
                e.printStackTrace();
            }


                try {
                    bw = new BufferedWriter(new FileWriter(Path1));
                    for (int m = 0; m < EdgeHistograms.size(); m++) {
                        bw.write(EdgeHistograms.get(m));
                        bw.newLine();
                        bw.flush();
                    }
                    bw.close();
                } catch (IOException e) {
                    e.printStackTrace();
                }
                try {
                    bw = new BufferedWriter(new FileWriter(Path2));
                    for (int m = 0; m < ColorLayouts.size(); m++) {
                        bw.write(ColorLayouts.get(m));
                        bw.newLine();
                        bw.flush();
                    }
                    bw.close();
                } catch (IOException e) {
                    e.printStackTrace();
                }
                try {
                    bw = new BufferedWriter(new FileWriter(Path3));
                    for (int m = 0; m < ScalableColors.size(); m++) {
                        bw.write(ScalableColors.get(m));
                        bw.newLine();
                        bw.flush();
                    }
                    bw.close();
                } catch (IOException e) {
                    e.printStackTrace();
                }


            i += 1;
        }
        System.out.println(1);
    }
    public void testSingleFile() throws IOException {
        EdgeHistogram e = new EdgeHistogram();
        e.extract(ImageIO.read(new File("wipo_us_ken.jpg")));
        System.out.println(Arrays.toString(e.getFeatureVector()));
        System.out.println(Arrays.toString(e.getByteArrayRepresentation()));

        e.extract(ImageIO.read(new File("wipo_us_fita.jpg")));
        System.out.println(Arrays.toString(e.getFeatureVector()));
        System.out.println(Arrays.toString(e.getByteArrayRepresentation()));
    }

    public void testExtraction() throws IOException {
        ArrayList<File> files = FileUtils.getAllImageFiles(new File("testdata/ferrari"), true);
        for (Iterator<File> iterator = files.iterator(); iterator.hasNext(); ) {
            File next = iterator.next();
            BufferedImage image = ImageIO.read(next);
            EdgeHistogram eh1 = new EdgeHistogram();
            EdgeHistogram eh2 = new EdgeHistogram();

            eh1.extract(image);
            System.out.println(" = " + Arrays.toString(eh1.getFeatureVector()));
            System.out.println(eh1.getFeatureVector().length);
            eh2.setByteArrayRepresentation(eh1.getByteArrayRepresentation());

        }
    }
/*
    public void testSerializationAndReUse() throws IOException, IllegalAccessException, InstantiationException {
        LireFeature f = new EdgeHistogram();
        String[] testFiles = new String[]{"D:\\DataSets\\WIPO-CA\\converted-0\\1001557.png",
                "D:\\DataSets\\WIPO-CA\\converted-0\\1001714.png",
                "D:\\DataSets\\WIPO-CA\\converted-0\\1001816.png",
                "D:\\DataSets\\WIPO-CA\\converted-0\\1001651.png",
                "D:\\DataSets\\WIPO-CA\\converted-0\\1002071.png",
                "D:\\DataSets\\WIPO-CA\\converted-0\\1001809.png",
                "D:\\DataSets\\WIPO-CA\\converted-0\\1001627.png",
                "D:\\DataSets\\WIPO-CA\\converted-0\\1001611.png",
                "D:\\DataSets\\WIPO-CA\\converted-0\\1001855.png",
                "D:\\DataSets\\WIPO-CA\\converted-0\\1002011.png"};
        for (String testFile : testFiles) {
//            f=new EdgeHistogram();
            f.extract(ImageIO.read(new File(testFile)));
            LireFeature f2 = new EdgeHistogram();
//            f2.setByteArrayRepresentation(f.getByteArrayRepresentation(), 0, f.getByteArrayRepresentation().length);
            f2.extract(ImageIO.read(new File(testFile)));
//            f2.getByteArrayRepresentation();
            System.out.println(testFile);
            System.out.println(Arrays.toString(f.getDoubleHistogram()).replaceAll("\\.0,",""));
            System.out.println(Arrays.toString(f2.getDoubleHistogram()).replaceAll("\\.0,", ""));
            System.out.println(f2.getDistance(f));
//            assertEquals(f2.getDistance(f), 0d, 0.000000001);
        }
    }
*/
}

