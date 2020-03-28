library(flowCore)
library(flowDensity)

# load dataset into R by simply listing all files in input directory and saving
# them again into the output directory

kInput <- "output/samples"
kOutput <- "output/ungated"

inputFiles <- sapply(list.files(kInput, recursive = T), function(p) {file.path(kInput, p)})

logTransformList <- transformList(sapply(1:10, function(i){sprintf("FL%d INT LOG", i)}),
                                  logTransform())

GateSample <- function(inputData) {
  inputData
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
  dir.create(dirname(outputPath), recursive = T, showWarnings = F)

  inputData <- LoadSample(inputPath)
  processedData <- GateSample(inputData)
  SaveSample(processedData, outputPath)
}

lapply(inputFiles, function(f) { ProcessSample(f, kOutput) })
