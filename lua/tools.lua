--- Convert vararg ... to a normal table
function table.pack(...)
  return { n = select("#", ...), ... }
end
