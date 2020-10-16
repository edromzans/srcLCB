import cartopy.crs as ccrs
import cartopy.feature as cfeature
import matplotlib.pyplot as plt

# Sudeste expandido
xlon0 = -56.
xlon1 = -38.
ylat0 = -13.
ylat1 = -27.
###################

plt.figure()
ax = plt.axes(projection=ccrs.PlateCarree())
# ax.stock_img()
ax.coastlines()
ax.gridlines(draw_labels=True)
ax.set_extent((xlon0, xlon1, ylat0, ylat1))  # (x0, x1, y0, y1)

ax.add_feature(cfeature.BORDERS)
ax.add_feature(cfeature.STATES)

plt.show()
