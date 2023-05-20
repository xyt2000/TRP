package net.semanticmetadata.lire.imageanalysis;



import junit.framework.TestCase;
import net.semanticmetadata.lire.aggregators.AbstractAggregator;
import net.semanticmetadata.lire.aggregators.BOVW;
import net.semanticmetadata.lire.builders.GlobalDocumentBuilder;
import net.semanticmetadata.lire.builders.LocalDocumentBuilder;
import net.semanticmetadata.lire.builders.SimpleDocumentBuilder;
import net.semanticmetadata.lire.classifiers.Cluster;
import net.semanticmetadata.lire.imageanalysis.features.GlobalFeature;
import net.semanticmetadata.lire.imageanalysis.features.LocalFeatureExtractor;
import net.semanticmetadata.lire.imageanalysis.features.global.CEDD;
import net.semanticmetadata.lire.imageanalysis.features.local.opencvfeatures.CvSurfExtractor;
import net.semanticmetadata.lire.imageanalysis.features.local.simple.SimpleExtractor;
import net.semanticmetadata.lire.utils.FileUtils;

import javax.imageio.ImageIO;
import java.awt.image.BufferedImage;
import java.io.File;
import java.io.FileInputStream;
import java.io.IOException;
import java.util.ArrayList;
import java.util.Arrays;

/**
 * Created by Nektarios on 28/5/2015.
 *
 * @author Nektarios Anagnostopoulos, nek.anag@gmail.com
 * (c) 2015 by Nektarios Anagnostopoulos
 */
public class test{
    Class<? extends GlobalFeature> globalFeatureClass = CEDD.class;
    Class<? extends LocalFeatureExtractor> localFeatureClass = CvSurfExtractor.class;
    SimpleExtractor.KeypointDetector keypointDetector = SimpleExtractor.KeypointDetector.CVSURF;
    Class<? extends AbstractAggregator> aggregatorClass = BOVW.class;

    String imagePath = "./src/test/resources/images/";
    String codebookPath = "./src/test/resources/codebooks/";
    public static void main(String[] args) throws IOException, IllegalAccessException, InstantiationException {
        testExtraction();
    }
    public static void testExtraction() throws IllegalAccessException, IOException, InstantiationException {
        String imagePath = "./src/test/resources/images/";
        ArrayList<String> images = FileUtils.readFileLines(new File(imagePath), true);
        System.out.println();
        //testGlobalExtract(images);
        //testLocalExtract(images);
        testSimpleExtract(images);
    }

    public static void testGlobalExtract() throws IOException, IllegalAccessException, InstantiationException {
        String imagePath = "./src/test/resources/images/";
        ArrayList<String> images = FileUtils.readFileLines(new File(imagePath), true);
        testGlobalExtract(images);
    }

    public static void testGlobalExtract(ArrayList<String> images) throws IOException, IllegalAccessException, InstantiationException {
        Class<? extends GlobalFeature> globalFeatureClass = CEDD.class;
        GlobalFeature globalFeature = globalFeatureClass.newInstance();
        GlobalDocumentBuilder globalDocumentBuilder = new GlobalDocumentBuilder();

        BufferedImage image;
        double[] featureVector;
        long ms, totalTime = 0;
        for (String path : images) {
            image = ImageIO.read(new FileInputStream(path));
            ms = System.currentTimeMillis();
            globalDocumentBuilder.extractGlobalFeature(image, globalFeature);
            ms = System.currentTimeMillis() - ms;
            totalTime += ms;
            featureVector = globalFeature.getFeatureVector();

            System.out.println(String.format("%.2f",  (double) ms ) + " ms. ~ " + path.substring(path.lastIndexOf('\\') + 1) + " ~ " + Arrays.toString(featureVector));
        }
        System.out.println(globalFeature.getFeatureName() + " " + String.format("%.2f",  totalTime / (double) images.size()) + " ms each.");
        System.out.println();
    }

    public static void testLocalExtract() throws IOException, IllegalAccessException, InstantiationException {
        Class<? extends GlobalFeature> globalFeatureClass = CEDD.class;
        Class<? extends LocalFeatureExtractor> localFeatureClass = CvSurfExtractor.class;
        SimpleExtractor.KeypointDetector keypointDetector = SimpleExtractor.KeypointDetector.CVSURF;
        Class<? extends AbstractAggregator> aggregatorClass = BOVW.class;

        String imagePath = "./src/test/resources/images/";
        String codebookPath = "./src/test/resources/codebooks/";
        ArrayList<String> images = FileUtils.readFileLines(new File(imagePath), true);
        testLocalExtract(images);
    }

    public static void testLocalExtract(ArrayList<String> images) throws IOException, IllegalAccessException, InstantiationException {
        Class<? extends GlobalFeature> globalFeatureClass = CEDD.class;
        Class<? extends LocalFeatureExtractor> localFeatureClass = CvSurfExtractor.class;
        SimpleExtractor.KeypointDetector keypointDetector = SimpleExtractor.KeypointDetector.CVSURF;
        Class<? extends AbstractAggregator> aggregatorClass = BOVW.class;

        String imagePath = "./src/test/resources/images/";
        String codebookPath = "./src/test/resources/codebooks/";
        LocalFeatureExtractor localFeatureExtractor = localFeatureClass.newInstance();
        LocalDocumentBuilder localDocumentBuilder = new LocalDocumentBuilder();
        AbstractAggregator aggregator = aggregatorClass.newInstance();

        Cluster[] codebook32 = Cluster.readClusters(codebookPath + "CvSURF32");
        Cluster[] codebook128 = Cluster.readClusters(codebookPath + "CvSURF128");

        BufferedImage image;
        double[] featureVector;
        long ms, totalTime = 0;
        for (String path : images) {
            image = ImageIO.read(new FileInputStream(path));
            ms = System.currentTimeMillis();
            localDocumentBuilder.extractLocalFeatures(image, localFeatureExtractor);
            aggregator.createVectorRepresentation(localFeatureExtractor.getFeatures(), codebook32);
            ms = System.currentTimeMillis() - ms;
            totalTime += ms;
            featureVector = aggregator.getVectorRepresentation();

            System.out.println(String.format("%.2f",  (double) ms ) + " ms. ~ " + path.substring(path.lastIndexOf('\\') + 1) + " ~ " + Arrays.toString(featureVector));
        }
        System.out.println(localFeatureExtractor.getClassOfFeatures().newInstance().getFeatureName() + " " + String.format("%.2f",  totalTime / (double) images.size()) + " ms each.");
        System.out.println();
    }

    public static void testSimpleExtract() throws IOException, IllegalAccessException, InstantiationException {
        Class<? extends GlobalFeature> globalFeatureClass = CEDD.class;
        Class<? extends LocalFeatureExtractor> localFeatureClass = CvSurfExtractor.class;
        SimpleExtractor.KeypointDetector keypointDetector = SimpleExtractor.KeypointDetector.CVSURF;
        Class<? extends AbstractAggregator> aggregatorClass = BOVW.class;

        String imagePath = "./src/test/resources/images/";
        String codebookPath = "./src/test/resources/codebooks/";
        ArrayList<String> images = FileUtils.readFileLines(new File(imagePath), true);
        testSimpleExtract(images);
    }

    public static void testSimpleExtract(ArrayList<String> images) throws IOException, IllegalAccessException, InstantiationException {
        Class<? extends GlobalFeature> globalFeatureClass = CEDD.class;
        Class<? extends LocalFeatureExtractor> localFeatureClass = CvSurfExtractor.class;
        SimpleExtractor.KeypointDetector keypointDetector = SimpleExtractor.KeypointDetector.CVSURF;
        Class<? extends AbstractAggregator> aggregatorClass = BOVW.class;

        String imagePath = "./src/test/resources/images/";
        String codebookPath = "./src/test/resources/codebooks/";
        SimpleExtractor simpleExtractor = new SimpleExtractor(globalFeatureClass.newInstance(), keypointDetector);
        SimpleDocumentBuilder simpleDocumentBuilder = new SimpleDocumentBuilder();
        AbstractAggregator aggregator = aggregatorClass.newInstance();

        Cluster[] codebook32 = Cluster.readClusters(codebookPath + "SIMPLEdetCVSURFCEDD32");
        Cluster[] codebook128 = Cluster.readClusters(codebookPath + "SIMPLEdetCVSURFCEDD128");

        BufferedImage image;
        double[] featureVector;
        long ms, totalTime = 0;
        for (String path : images) {
            image = ImageIO.read(new FileInputStream(path));
            ms = System.currentTimeMillis();
            simpleDocumentBuilder.extractLocalFeatures(image, simpleExtractor);
            aggregator.createVectorRepresentation(simpleExtractor.getFeatures(), codebook32);
            ms = System.currentTimeMillis() - ms;
            totalTime += ms;
            featureVector = aggregator.getVectorRepresentation();

            System.out.println(String.format("%.2f",  (double) ms ) + " ms. ~ " + path.substring(path.lastIndexOf('\\') + 1) + " ~ " + Arrays.toString(featureVector));
        }
        System.out.println(simpleExtractor.getFeatureName() + " " + String.format("%.2f",  totalTime / (double) images.size()) + " ms each.");
        System.out.println();
    }

}

