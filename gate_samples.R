library(flowCore)
library(flowDensity)

# load dataset into R by simply listing all files in input directory and saving
# them again into the output directory

kInput <- "output/samples"
kOutput <- "output/gated_single"

kChannels1 <- c("CD45-KrOr", "SS INT LIN")
kPosition1 <- c(T, F)
kChannels2 <- c("CD19-APCA750", "SS INT LIN")
kPosition2 <- c(T, F)

inputFiles <- sapply(list.files(kInput, recursive = T, pattern = "\\.LMD$"), function(p) {file.path(kInput, p)})

logTransformList <- transformList(sapply(1:10, function(i){sprintf("FL%d INT LOG", i)}),
                                  logTransform())

GateSample <- function(inputData, plotPath) {
  chNames <- inputData@parameters@data$name
  names(chNames) <- inputData@parameters@data$desc
  chKeys1 <- as.character(chNames[kChannels1])
  chKeys2 <- as.character(chNames[kChannels2])
  gatedData1 <- flowDensity(inputData, channels = chKeys1, position = kPosition1)
  # gatedData2 <- flowDensity(gatedData1, channels = chKeys2, position = kPosition2, use.percentile = c(F, F), percentile = c(.25, .95))

  jpeg(file.path(plotPath, "gate1.jpeg"))
    plot(inputData, gatedData1)
  dev.off()
  # jpeg(file.path(plotPath, "gate2.jpeg"))
  #   plot(inputData, gatedData2)
  # dev.off()

  getflowFrame(gatedData1)
}

LoadSample <- function(inputPath) {
  cat(inputPath, "\n")
  # load data linearized
  data <- read.FCS(inputPath, transformation = "linearize", dataset = 1)

  # apply log scaling to all channels besides SS and FS
  data <- transform(data, logTransformList)
  data
}

SaveSample <- function(data, outputPath) {
  write.FCS(data, outputPath)
}

ProcessSample <- function(inputPath, outputDir) {
  outputPath <- file.path(outputDir, substr(inputPath, nchar(kInput) + 2, nchar(inputPath) + 1))
  plotPath <- file.path(outputDir, "plots", substr(inputPath, nchar(kInput) + 2, nchar(inputPath) + 1))
  plotPath <- gsub(".LMD", "", plotPath)

  dir.create(dirname(outputPath), recursive = T, showWarnings = F)
  dir.create(plotPath, recursive = T, showWarnings = F)

  inputData <- LoadSample(inputPath)
  tryCatch({
    processedData <- GateSample(inputData, plotPath)
    SaveSample(processedData, outputPath)
  }, error = function(e) {
    show(e)
  })
}

# ProcessSample(inputFiles[1], kOutput)
lapply(inputFiles, function(f) { ProcessSample(f, kOutput) })
