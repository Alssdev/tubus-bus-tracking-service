from shapely import Point

def get_segment_of_route(bus_route, start, end):
  # find the segment by accumulating points between start and end points
  route_coords = list(bus_route.coords)
  segment_coords = []  # Begin with the interpolated start point
  segment_aux = [start]

  # distances
  start_distance = bus_route.project(Point(start))
  end_distance = bus_route.project(Point(end))

  # Add points in between start and end points based on their projected distances
  for coord in route_coords:
      point = Point(coord)
      dist = bus_route.project(point)

      if start_distance < end_distance:
        if start_distance < dist < end_distance:
            segment_coords.append(coord)
      elif start_distance < dist < bus_route.length:
          segment_aux.append(coord)
      elif dist < end_distance:
        segment_coords.append(coord)

  segment_aux.extend(segment_coords)
  segment_coords = segment_aux

  # end with the interpolated end point
  segment_coords.append(end)
  return [(e[1], e[0]) for e in segment_coords]
