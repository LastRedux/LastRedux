const numberWithCommas = num => {
  return num.toString().replace(/(\d)(?=(\d{3})+(?!\d))/g, '$1,');
}

const abbreviateNumber = num => {
  if (parseInt(num) !== num) {
    // Value passed isn't a number, probably a placeholder like '---'
    return num
  }
  
  if (num < 1e3) return num;
  if (num >= 1e3 && num < 1e6) return +(num / 1e3).toFixed(1) + 'K';
  if (num >= 1e6 && num < 1e9) return +(num / 1e6).toFixed(1) + 'M';
  if (num >= 1e9 && num < 1e12) return +(num / 1e9).toFixed(1) + 'B';
  if (num >= 1e12) return +(num / 1e12).toFixed(1) + 'T';
}