export function toPascal(string, delimiter) {
  delimiter = !!delimiter ? delimiter : " "

  return string.split(delimiter)
               .map(word => word.charAt(0)
                                .toUpperCase() + word.slice(1))
               .join(" ")
}

export function decimalToPercent(value, precision) {
  precision = !!precision ? precision : Math.pow(10, 2)
  return Math.ceil(parseFloat(value) * 100 * precision) / precision
}
